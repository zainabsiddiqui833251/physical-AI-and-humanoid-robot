# --- Standard ---
import os
import uuid

# --- FastAPI ---
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel

# --- LangChain 2.x ---
# LangChain 2.x imports
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.qdrant import Qdrant   # <- use qdrant submodule
from langchain.prompts import ChatPromptTemplate   # <- no .chat in 2.x
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableSequence

# --- Database ---
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, insert, select, and_, update
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

# --- Load environment variables ---
load_dotenv()

# --- Initialize FastAPI ---
app = FastAPI()

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/speckit_db")

try:
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()

    chat_logs_table = Table('chat_logs', metadata, autoload_with=engine)
    book_pages_table = Table('book_pages', metadata, autoload_with=engine)
    page_embeddings_table = Table('page_embeddings', metadata, autoload_with=engine)

    # --- Helper functions ---
    def to_langchain_message(msg_dict):
        if msg_dict.get("type") == "human":
            return HumanMessage(content=msg_dict.get("content"))
        elif msg_dict.get("type") == "ai":
            return AIMessage(content=msg_dict.get("content"))
        elif msg_dict.get("type") == "system":
            return SystemMessage(content=msg_dict.get("content"))
        return None

    def to_frontend_message(message):
        if isinstance(message, HumanMessage):
            return {"type": "human", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"type": "ai", "content": message.content}
        elif isinstance(message, SystemMessage):
            return {"type": "system", "content": message.content}
        return None

    async def get_chat_history_from_db(user_id: str, session_id: str):
        if not chat_logs_table:
            return []
        with engine.connect() as connection:
            stmt = select(chat_logs_table).where(
                and_(
                    chat_logs_table.c.user_id == user_id,
                    chat_logs_table.c.session_id == session_id
                )
            ).order_by(chat_logs_table.c.timestamp)
            result = connection.execute(stmt)
            history = []
            for row in result:
                msg_dict = {
                    "type": row.role,
                    "content": row.content,
                    "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                    "context_page_id": row.context_page_id,
                    "context_embedding_id": row.context_embedding_id
                }
                history.append(msg_dict)
            return history

    async def save_chat_message_to_db(user_id: str, session_id: str, role: str, content: str, context_page_id=None, context_embedding_id=None):
        if not chat_logs_table:
            return
        with engine.connect() as connection:
            stmt = insert(chat_logs_table).values(
                user_id=user_id,
                session_id=session_id,
                role=role,
                content=content,
                context_page_id=context_page_id,
                context_embedding_id=context_embedding_id,
                timestamp=func.now()
            )
            connection.execute(stmt)
            connection.commit()

except Exception as e:
    print(f"Database connection error: {e}")
    engine = None
    chat_logs_table = None
    book_pages_table = None
    page_embeddings_table = None

# --- Qdrant Retriever ---
QDRANT_COLLECTION_NAME = "humanoid-robotics-book"

def get_retriever():
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([qdrant_url, qdrant_api_key, openai_api_key]):
        raise ValueError("Missing Qdrant or OpenAI API keys in environment.")

    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    try:
        qdrant_client = Qdrant.from_existing_collection(
            url=qdrant_url,
            api_key=qdrant_api_key,
            collection_name=QDRANT_COLLECTION_NAME,
            embedding=embeddings
        )
        return qdrant_client.as_retriever()
    except Exception as e:
        print(f"Qdrant initialization error: {e}")
        raise RuntimeError(f"Could not initialize Qdrant retriever: {e}")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- Pydantic Model ---
class ChatRequest(BaseModel):
    query: str
    history: list = []
    session_id: str | None = None
    user_id: str | None = None

# --- API Endpoint ---
@app.post("/api/chat")
async def chat(chat_request: ChatRequest):
    try:
        session_id = chat_request.session_id or str(uuid.uuid4())
        user_id = chat_request.user_id or "anonymous_user"

        # --- Load History ---
        if engine and chat_logs_table:
            db_history_dicts = await get_chat_history_from_db(user_id, session_id)
            chat_history = [to_langchain_message(msg) for msg in db_history_dicts if to_langchain_message(msg)]
        else:
            chat_history = [to_langchain_message(msg) for msg in chat_request.history if to_langchain_message(msg)]

        # --- Retriever & LLM ---
        retriever = get_retriever()
        llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo", temperature=0.7)

        # --- Prompt Template ---
        template = """
        You are a helpful assistant for the Humanoid Robotics Book.
        Answer the question based only on the following context:
        {context}
        If you don't know the answer, just say you don't know.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", "{question}")
        ])

        # --- RAG Chain ---
        rag_chain = RunnableSequence(
            {
                "context": lambda x: format_docs(retriever.get_relevant_documents(x["question"])),
                "question": lambda x: x["question"],
                "chat_history": lambda x: x["chat_history"]
            },
            prompt,
            llm,
            StrOutputParser()
        )

        response_content = rag_chain.invoke({
            "question": chat_request.query,
            "chat_history": chat_history
        })

        # --- Save to DB ---
        if engine and chat_logs_table:
            await save_chat_message_to_db(user_id, session_id, "user", chat_request.query)
            await save_chat_message_to_db(user_id, session_id, "assistant", response_content)

        return {"response": response_content, "session_id": session_id, "user_id": user_id}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/api")
async def root():
    return {"message": "RAG Chatbot API is running with PostgreSQL history persistence."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

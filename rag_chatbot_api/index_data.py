import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DOCUSAURUS_DOCS_PATH = "Humanoid_robotics_book/docs"
QDRANT_COLLECTION_NAME = "humanoid-robotics-book"

def index_documents():
    """
    Loads documents from the Docusaurus `docs` directory, splits them into chunks,
    generates embeddings, and indexes them in a Qdrant collection.
    """
    print("Loading documents...")
    loader = DirectoryLoader(
        DOCUSAURUS_DOCS_PATH,
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
        show_progress=True,
        use_multithreading=True,
    )
    documents = loader.load()

    if not documents:
        print("No documents found. Please check the DOCUSAURUS_DOCS_PATH.")
        return

    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks.")

    print("Generating embeddings and indexing in Qdrant...")
    # Get Qdrant URL and API key from environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in the .env file.")

    # Get OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be set in the .env file.")

    embeddings = OpenAIEmbeddings(api_key=openai_api_key)

    # Create the Qdrant collection
    Qdrant.from_documents(
        splits,
        embeddings,
        url=qdrant_url,
        api_key=qdrant_api_key,
        collection_name=QDRANT_COLLECTION_NAME,
        prefer_grpc=True, # Use gRPC for better performance
        force_recreate=True, # Set to False if you want to update an existing collection
    )

    print("Indexing complete!")

if __name__ == "__main__":
    index_documents()

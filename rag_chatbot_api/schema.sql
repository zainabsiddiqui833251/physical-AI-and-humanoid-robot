-- Table to store book page metadata and content
CREATE TABLE IF NOT EXISTS book_pages (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2048) UNIQUE NOT NULL,
    title VARCHAR(512),
    content TEXT NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table to store text chunks and their embeddings
CREATE TABLE IF NOT EXISTS page_embeddings (
    id SERIAL PRIMARY KEY,
    page_id INTEGER NOT NULL REFERENCES book_pages(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL -- Assuming OpenAI's 1536-dimensional embeddings
);

-- Table to store user chat history
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL, -- To group messages from the same conversation
    user_query TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

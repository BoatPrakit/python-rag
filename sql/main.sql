CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    text TEXT,
    vector vector(1024)  -- 1024 is the embedding size of BAAI/bge-m3
);
from sentence_transformers import SentenceTransformer
import os
import psycopg2

ENV = {
    "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT"),
}

# Connect to PostgreSQL
conn = psycopg2.connect(f'dbname={ENV["POSTGRES_DB"]} user={ENV["POSTGRES_USER"]} password={ENV["POSTGRES_PASSWORD"]} host=localhost port={ENV["POSTGRES_PORT"]}')
cur = conn.cursor()

def insert_document(text, vector):
    # Insert text and vector into the database
    cur.execute("INSERT INTO documents (text, vector) VALUES (%s, %s)", (text, vector.tolist()))
    conn.commit()

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("BAAI/bge-m3")

# The sentences to encode
sentences = "Hello world"

# 2. Calculate embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print(embeddings.tolist())
# insert_embedding(sentences, embeddings)
# print(embeddings.shape)
# [3, 384]

# 3. Calculate the embedding similarities
# similarities = model.similarity(embeddings, embeddings)
# print(similarities)
# tensor([[1.0000, 0.6660, 0.1046],
#         [0.6660, 1.0000, 0.1411],
#         [0.1046, 0.1411, 1.0000]])

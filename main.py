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

def get_documents(vector):
    # Get documents from the database
    cur.execute("SELECT text, vector FROM documents WHERE vector <-> %s", (vector.tolist(),))
    return cur.fetchall()

def close_connection():
    # Close the database connection
    cur.close()
    conn.close()

# 1. Load a pretrained Sentence Transformer model
def load_model():
    if os.path.exists("./models/bge-m3"):
        return SentenceTransformer("./models/bge-m3")
    else:
        model = SentenceTransformer("BAAI/bge-m3")
        model.save("./models/bge-m3")
        return model

model = load_model()

# The sentences to encode
sentences = "aaa"

# 2. Calculate embeddings by calling model.encode()
embeddings = model.encode(sentences)
# embedding2 = get_documents("Hell")
# print(embeddings.tolist())
insert_document(sentences, embeddings)
# print(embeddings.shape)

# 3. Calculate the embedding similarities
# similarities = model.similarity(embeddings, embeddings)
# print(similarities.tolist())
# tensor([[1.0000, 0.6660, 0.1046],
#         [0.6660, 1.0000, 0.1411],
#         [0.1046, 0.1411, 1.0000]])

close_connection()


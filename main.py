import ollama
from sentence_transformers import SentenceTransformer
import os
import psycopg2
from ollama import chat

# 1. Load a pretrained Sentence Transformer model
def load_model():
    if os.path.exists("./models/bge-m3"):
        return SentenceTransformer("./models/bge-m3")
    else:
        model = SentenceTransformer("BAAI/bge-m3")
        model.save("./models/bge-m3")
        return model

model = load_model()

ENV = {
    "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT"),
}

# Connect to PostgreSQL
conn = psycopg2.connect(f'dbname={ENV["POSTGRES_DB"]} user={ENV["POSTGRES_USER"]} password={ENV["POSTGRES_PASSWORD"]} host=localhost port={ENV["POSTGRES_PORT"]}')
cur = conn.cursor()

def insert_document(text):
    # Insert text and vector into the database
    vector = model.encode(text).tolist()
    cur.execute("INSERT INTO documents (text, vector) VALUES (%s, %s)", (text, vector))
    conn.commit()

def get_documents(text, limit=5):
    # Get documents from the database
    vector = model.encode(text).tolist()
    embedding = "[" + ", ".join(map(str, vector)) + "]"
    cur.execute("SELECT text, vector <=> %s::vector AS similarity  FROM documents ORDER BY similarity ASC LIMIT %s", (embedding, limit))
    return cur.fetchall()

def close_connection():
    # Close the database connection
    cur.close()
    conn.close()


# ss = [
#     "ต้มยำกุ้งถือกำเนิดในภาคกลางของประเทศไทย และเป็นอาหารที่มีรสจัด",
#     "ข้าวซอยเป็นอาหารพื้นเมืองของภาคเหนือ มีต้นกำเนิดจากวัฒนธรรมจีน-มุสลิม",
#     "หมูปิ้งเริ่มเป็นที่นิยมในกรุงเทพฯ ช่วงปี 2520 และกลายเป็นอาหารเช้ายอดฮิต",
#     "ส้มตำไทยได้รับอิทธิพลจากลาว แต่ได้รับการปรับรสชาติให้เหมาะกับคนไทย",
#     "แกงเขียวหวานถือกำเนิดขึ้นในสมัยอยุธยา โดยได้รับอิทธิพลจากเครื่องเทศอินเดีย"
# ]
# for s in ss:
#     insert_document(s)
# The sentences to encode
sentences = "มุสลิมคืออะไร"

# 2. Calculate embeddings by calling model.encode()
embedding2 = get_documents(sentences)

response = ollama.chat(model="llama3.1", messages=[
    {"role": "system", "content": "You are a assistant, use the following information to answer the user's question: " + str(embedding2)},
    {"role": "user", "content": sentences}
])

print(response)

close_connection()

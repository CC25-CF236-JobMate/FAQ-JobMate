from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- PERUBAHAN DI SINI: Impor library CORS
import json
import re
import torch
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
from sklearn.preprocessing import normalize
import random

app = Flask(__name__)
CORS(app)  # <--- PERUBAHAN DI SINI: Terapkan CORS ke aplikasi Flask Anda

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load IndoBERT model & tokenizer sekali saat startup
print("Loading IndoBERT model...")
model_name = "indolem/indobert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()
print("Model loaded.")

# Load dataset FAQ
print("Loading and processing FAQ dataset...")
with open("dataset/qnaJobMate.json", "r", encoding="utf-8") as f:
    data = json.load(f)

all_questions = []
all_answers = []

for item in data:
    question_variants = [item['question']] + item.get('paraphrases', [])
    question_variants = [preprocess_text(q) for q in question_variants]
    answer_variants = [item['answer']] + item.get('answer_paraphrases', [])
    for q in question_variants:
        all_questions.append(q)
        all_answers.append(answer_variants)
print("Dataset processed.")

def encode(text_list):
    embeddings = []
    with torch.no_grad():
        for text in text_list:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64)
            outputs = model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
            embeddings.append(cls_embedding[0])
    embeddings = np.array(embeddings)
    embeddings = normalize(embeddings)
    return embeddings

print("Encoding FAQ questions for Faiss index...")
question_embeddings = encode(all_questions)
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(question_embeddings)
print("Faiss index created successfully.")

def chatbot_response(user_question, threshold=0.8, top_k=1):
    user_question = preprocess_text(user_question)
    user_emb = encode([user_question])
    D, I = index.search(user_emb, top_k)
    best_idx = I[0][0]
    confidence = D[0][0]
    if confidence < threshold:
        return "Maaf, saya tidak paham pertanyaan Anda.", float(confidence)
    else:
        possible_answers = all_answers[best_idx]
        response = random.choice(possible_answers)
        return response, float(confidence)

@app.route("/faq", methods=["POST"])
def faq():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400
    try:
        answer, confidence = chatbot_response(question)
        return jsonify({
            "answer": answer,
            "confidence": confidence
        })
    except Exception as e:
        app.logger.error(f"Error processing question: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# <--- PERUBAHAN DI SINI: Tambahkan endpoint health check
@app.route("/health", methods=["GET"])
def health_check():
    """
    Endpoint untuk memeriksa apakah layanan berjalan dengan baik.
    Frontend menggunakan ini untuk menampilkan status 'Online'.
    """
    return jsonify({"status": "ok"}), 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

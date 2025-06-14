from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import torch
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
from sklearn.preprocessing import normalize
import random
import os # <--- PERUBAHAN BARU

# --- PERUBAHAN BARU: Impor dan Konfigurasi Gemini ---
import google.generativeai as genai

# Konfigurasi API Key dari environment variable
# Di terminal Anda, jalankan: export GOOGLE_API_KEY="API_KEY_ANDA"
# Untuk Windows: set GOOGLE_API_KEY="API_KEY_ANDA"
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # Inisialisasi model Gemini
    gemini_model = genai.GenerativeModel('gemini-1.5-flash') # Gunakan model yang efisien
    print("Gemini model loaded successfully.")
except KeyError:
    print("===============================================================")
    print("WARNING: GOOGLE_API_KEY environment variable not set.")
    print("Gemini integration will be disabled.")
    print("===============================================================")
    gemini_model = None
# --- AKHIR PERUBAHAN BARU ---


app = Flask(__name__)
CORS(app)

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
all_original_questions = [] # <--- PERUBAHAN BARU: Simpan pertanyaan asli untuk konteks

for item in data:
    question_variants = [item['question']] + item.get('paraphrases', [])
    processed_variants = [preprocess_text(q) for q in question_variants]
    answer_variants = [item['answer']] + item.get('answer_paraphrases', [])
    for i, q_proc in enumerate(processed_variants):
        all_questions.append(q_proc)
        all_answers.append(answer_variants)
        all_original_questions.append(question_variants[i]) # <--- PERUBAHAN BARU

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

# --- PERUBAHAN BARU: Fungsi untuk memanggil Gemini ---
def ask_gemini(question, context=""):
    if not gemini_model:
        return "Maaf, fitur AI canggih sedang tidak tersedia saat ini.", "N/A"

    # Ini adalah bagian "Prompt Engineering"
    # Kita memberi instruksi kepada Gemini agar berperan sebagai asisten JobMate
    prompt = f"""
    Anda adalah "JobMate Assistant", sebuah chatbot yang sangat ramah dan membantu untuk platform pencari kerja bernama JobMate.
    Tugas Anda adalah menjawab pertanyaan pengguna seputar penggunaan platform JobMate.
    Jawablah dengan bahasa Indonesia yang santai dan bersahabat.

    KONTEKS TAMBAHAN (jika relevan): "{context}"

    PERTANYAAN PENGGUNA: "{question}"

    JAWABAN ANDA:
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text, "Generated by Gemini"
    except Exception as e:
        app.logger.error(f"Error calling Gemini API: {e}")
        return "Maaf, terjadi sedikit kendala saat mencoba menjawab. Silakan coba lagi.", "Error"
# --- AKHIR PERUBAHAN BARU ---


def chatbot_response(user_question, threshold=0.85, top_k=1): # <--- PERUBAHAN BARU: Naikkan threshold
    processed_question = preprocess_text(user_question)
    user_emb = encode([processed_question])
    D, I = index.search(user_emb, top_k)
    best_idx = I[0][0]
    confidence = D[0][0]

    if confidence >= threshold:
        # Jika confidence tinggi, gunakan jawaban dari database
        possible_answers = all_answers[best_idx]
        response = random.choice(possible_answers)
        return response, float(confidence), "faiss_retrieval" # Memberi tahu sumber jawaban
    else:
        # Jika confidence rendah, lempar ke Gemini
        # Berikan konteks dari jawaban yang "hampir" cocok untuk membantu Gemini
        context_answer = random.choice(all_answers[best_idx])
        original_question_context = all_original_questions[best_idx]
        full_context = f"Pengguna mungkin bertanya tentang '{original_question_context}', yang jawabannya adalah: '{context_answer}'"
        
        # Panggil Gemini untuk jawaban yang lebih cerdas
        response, source = ask_gemini(user_question, context=full_context)
        return response, float(confidence), source


@app.route("/faq", methods=["POST"])
def faq():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400
    try:
        # Perhatikan ada 3 nilai yang dikembalikan sekarang
        answer, confidence, source = chatbot_response(question)
        return jsonify({
            "answer": answer,
            "confidence": confidence,
            "source": source # <--- PERUBAHAN BARU: Tambahkan sumber jawaban
        })
    except Exception as e:
        app.logger.error(f"Error processing question: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
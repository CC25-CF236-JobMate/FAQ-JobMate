# JobMate FAQ Chatbot API

JobMate FAQ Chatbot adalah sistem chatbot berbasis AI yang menggunakan **IndoBERT untuk semantic similarity** dan **Google Gemini AI untuk intelligent responses**. Sistem ini memberikan pengalaman chat yang lebih pintar dengan menggabungkan retrieval-based responses untuk pertanyaan FAQ yang umum dan generative AI untuk pertanyaan yang lebih kompleks atau tidak terdapat dalam database.

## 🚀 Features

- **Hybrid AI System**: Kombinasi IndoBERT semantic search + Google Gemini generative AI
- **Smart Response Selection**: Otomatis memilih antara database FAQ atau AI generation berdasarkan confidence score
- **Semantic Search**: Menggunakan IndoBERT untuk memahami konteks pertanyaan
- **Fast Retrieval**: FAISS indexing untuk pencarian jawaban yang cepat
- **Intelligent Fallback**: Gemini AI untuk menjawab pertanyaan di luar database FAQ
- **Context-Aware AI**: Memberikan konteks dari database kepada Gemini untuk jawaban yang lebih relevan
- **Multiple Answer Variants**: Mendukung variasi jawaban untuk respons yang lebih natural
- **Question Paraphrasing**: Dapat memahami berbagai cara bertanya yang sama
- **RESTful API**: Interface yang mudah diintegrasikan
- **Health Check**: Endpoint untuk monitoring status sistem
- **CORS Support**: Mendukung akses dari berbagai domain
- **Response Source Tracking**: Melacak sumber jawaban (database vs AI generated)

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  IndoBERT Model  │───▶│ FAISS Index     │
│                 │    │  (Tokenization   │    │ (Similarity     │
│                 │    │   & Embedding)   │    │  Search)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                          │
┌─────────────────┐    ┌──────────────────┐              │
│ Confidence      │◀───│  Confidence      │◀─────────────┘
│ Check           │    │  Evaluation      │
│ (Threshold=0.85)│    │                  │
└─────────────────┘    └──────────────────┘
          │                        │
          ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│ High Confidence │    │ Low Confidence   │
│ (≥0.85)         │    │ (<0.85)          │
│                 │    │                  │
│ ┌─────────────┐ │    │ ┌──────────────┐ │
│ │Database FAQ │ │    │ │ Gemini AI    │ │
│ │Response     │ │    │ │ + Context    │ │
│ └─────────────┘ │    │ └──────────────┘ │
└─────────────────┘    └──────────────────┘
          │                        │
          └────────┬─────────────────┘
                   ▼
           ┌─────────────────┐
           │ Final Response  │
           │ + Source Info   │
           │ + Confidence    │
           └─────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Google API Key untuk Gemini AI
- Google Cloud Platform account (untuk deployment)
- Docker (opsional untuk containerization)

## 🛠️ Installation

### Local Development

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd jobmate-faq-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Google Gemini API**
   
   **Untuk Linux/Mac:**
   ```bash
   export GOOGLE_API_KEY="your_gemini_api_key_here"
   ```
   
   **Untuk Windows:**
   ```cmd
   set GOOGLE_API_KEY="your_gemini_api_key_here"
   ```
   
   **Atau buat file .env:**
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Prepare dataset**
   - Pastikan file `dataset/qnaJobMate.json` tersedia
   - Format dataset harus sesuai dengan struktur yang diharapkan

6. **Run application locally**
   ```bash
   python main.py
   ```

   Server akan berjalan di `http://localhost:8080`

## 🤖 AI System Behavior

### Response Strategy

1. **High Confidence (≥0.85)**: Menggunakan jawaban dari database FAQ
   - Cepat dan konsisten
   - Jawaban yang sudah terkurasi
   - Source: `faiss_retrieval`

2. **Low Confidence (<0.85)**: Menggunakan Gemini AI dengan konteks
   - AI generative dengan pemahaman konteks
   - Mampu menangani pertanyaan kompleks
   - Source: `Generated by Gemini`

3. **Fallback Mode**: Jika Gemini tidak tersedia
   - Sistem tetap berjalan dengan database FAQ saja
   - Warning message saat startup

## 📁 Project Structure

```
jobmate-faq-chatbot/
├── main.py                 # Aplikasi Flask utama dengan Gemini integration
├── requirements.txt        # Dependencies Python (termasuk google-generativeai)
├── Dockerfile             # Container configuration
├── dataset/
│   └── qnaJobMate.json    # Dataset FAQ
└── README.md              # Dokumentasi ini
```

## 📊 Dataset Format

Dataset FAQ harus dalam format JSON dengan struktur berikut:

```json
[
  {
    "question": "Apa itu JobMate?",
    "paraphrases": [
      "web apa ini",
      "ini web apa",
      "JobMate itu apa?",
      "Definisi JobMate?",
      "Pengertian JobMate?",
      "Apa yang dimaksud dengan JobMate?",
      "Jelaskan tentang JobMate",
      "JobMate adalah platform apa?",
      "Bisa tolong ceritakan tentang JobMate?",
      "Saya belum tahu JobMate, bisa dijelaskan?",
      "Penjelasan singkat mengenai JobMate",
      "JobMate merupakan aplikasi seperti apa sih?"
    ],
    "answer": "JobMate adalah platform online yang memudahkan pengguna untuk mencari lowongan pekerjaan, melamar langsung, dan menemukan pekerjaan yang paling cocok berdasarkan skill dan preferensi mereka.",
    "answer_paraphrases": [
      "Ini adalah Website JobMate, JobMate merupakan platform digital yang dirancang untuk membantu pencari kerja menemukan lowongan yang sesuai dengan keahlian dan keinginan mereka, sekaligus memungkinkan pengajuan lamaran secara langsung.",
      "Website ini adalah platform online bernama JobMate berfungsi sebagai penghubung antara pencari kerja dengan perusahaan, menyediakan kemudahan dalam pencarian lowongan dan proses melamar pekerjaan berdasarkan kriteria yang diinginkan.",
      "Website JobMate adalah layanan berbasis internet yang memfasilitasi proses pencarian kerja dengan menyediakan berbagai lowongan pekerjaan dan fitur lamaran langsung yang disesuaikan dengan profil dan preferensi pengguna.",
      "Website ini adalah platform pencarian kerja online bernama JobMate, JobMate menawarkan solusi komprehensif bagi pencari kerja untuk menemukan dan melamar pekerjaan yang relevan dengan latar belakang dan minat mereka."
    ]
  }
]
```

## 🔌 API Endpoints

### 1. FAQ Query
**POST** `/faq`

Endpoint untuk menanyakan pertanyaan kepada chatbot.

**Request Body:**
```json
{
  "question": "Bagaimana cara mencari kerja yang efektif?"
}
```

**Response (High Confidence - Database):**
```json
{
  "answer": "Untuk mencari kerja yang efektif, Anda bisa menggunakan fitur pencarian di JobMate...",
  "confidence": 0.92,
  "source": "faiss_retrieval"
}
```

**Response (Low Confidence - Gemini AI):**
```json
{
  "answer": "Untuk mencari kerja yang efektif, saya sarankan beberapa strategi: 1) Optimalkan profil LinkedIn Anda, 2) Gunakan platform seperti JobMate untuk mencari lowongan yang sesuai...",
  "confidence": 0.73,
  "source": "Generated by Gemini"
}
```

**Response (Gemini Error):**
```json
{
  "answer": "Maaf, terjadi sedikit kendala saat mencoba menjawab. Silakan coba lagi.",
  "confidence": 0.73,
  "source": "Error"
}
```

### 2. Health Check
**GET** `/health`

Endpoint untuk memeriksa status sistem.

**Response:**
```json
{
  "status": "ok"
}
```

## 🚀 Deployment

### Google Cloud Run

1. **Set environment variable untuk Gemini API**
   ```bash
   gcloud run services update faq-jobmate-api \
     --set-env-vars GOOGLE_API_KEY="your_api_key_here" \
     --region asia-southeast2
   ```

2. **Build dan push image ke Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/capstone-jobseeker-dd654/faq-jobmate-api:latest
   ```

3. **Deploy ke Cloud Run**
   ```bash
   gcloud run deploy faq-jobmate-api \
     --image gcr.io/capstone-jobseeker-dd654/faq-jobmate-api:latest \
     --region asia-southeast2 \
     --platform managed \
     --allow-unauthenticated \
     --min-instances 1 \
     --max-instances 1 \
     --timeout 300 \
     --cpu 2 \
     --memory 8Gi \
     --set-env-vars GOOGLE_API_KEY="your_api_key_here"
   ```

4. **Live URL**
   ```
   https://faq-jobmate-api-705829099986.asia-southeast2.run.app
   ```

### Docker (Alternative)

```bash
# Build image
docker build -t jobmate-faq-api .

# Run container dengan Gemini API key
docker run -p 8080:8080 -e GOOGLE_API_KEY="your_api_key_here" jobmate-faq-api
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Port aplikasi |
| `HOST` | 0.0.0.0 | Host binding |
| `GOOGLE_API_KEY` | - | **Required**: API key untuk Google Gemini |

### Model Configuration

- **IndoBERT Model**: `indolem/indobert-base-uncased`
- **Gemini Model**: `gemini-1.5-flash` (efisien dan cepat)
- **Max Length**: 64 tokens
- **Confidence Threshold**: 0.85 (dinaikkan untuk kualitas lebih baik)
- **Top K Results**: 1

### Confidence Threshold Strategy

- **≥0.85**: Gunakan database FAQ (jawaban cepat dan akurat)
- **<0.85**: Gunakan Gemini AI dengan konteks (jawaban yang lebih fleksibel)

## 🧪 Testing

### Test API menggunakan curl

```bash
# Test FAQ dengan pertanyaan dalam database
curl -X POST https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq \
  -H "Content-Type: application/json" \
  -d '{"question": "Apa itu JobMate?"}'

# Test FAQ dengan pertanyaan di luar database (akan menggunakan Gemini)
curl -X POST https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq \
  -H "Content-Type: application/json" \
  -d '{"question": "Bagaimana tips interview kerja yang baik?"}'

# Test health check
curl https://faq-jobmate-api-705829099986.asia-southeast2.run.app/health
```

### Test menggunakan Python

```python
import requests

# Test dengan pertanyaan yang ada di database
response = requests.post(
    'https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq',
    json={'question': 'Apa itu JobMate?'}
)
result = response.json()
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Source: {result['source']}")

# Test dengan pertanyaan yang akan ditangani Gemini
response = requests.post(
    'https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq',
    json={'question': 'Tips sukses dalam wawancara kerja?'}
)
result = response.json()
print(f"Answer: {result['answer']}")
print(f"Source: {result['source']}")
```

## 🔧 Troubleshooting

### Common Issues

1. **Gemini API Key Issues**
   ```
   WARNING: GOOGLE_API_KEY environment variable not set.
   Gemini integration will be disabled.
   ```
   **Solution**: Set environment variable dengan API key yang valid

2. **Memory Error**
   - Pastikan container memiliki memory yang cukup (minimal 8GB)
   - Reduce batch size jika diperlukan

3. **Model Loading Timeout**
   - Increase timeout setting di Cloud Run
   - Use persistent storage untuk model caching

4. **Low Confidence Scores**
   - Review dan expand dataset FAQ
   - Adjust similarity threshold (default: 0.85)
   - Add more question paraphrases

5. **Gemini API Quota Exceeded**
   - Monitor penggunaan API di Google Cloud Console
   - Implement rate limiting jika diperlukan
   - Consider caching untuk pertanyaan yang sering ditanya

## 📈 Performance Optimization

- **Model Caching**: Model dimuat sekali saat startup
- **Hybrid Response**: Otomatis memilih strategi terbaik berdasarkan confidence
- **FAISS Indexing**: Fast similarity search untuk database FAQ
- **Normalized Embeddings**: Improved search accuracy
- **Context-Aware AI**: Memberikan konteks relevan kepada Gemini
- **Graceful Fallback**: Sistem tetap berjalan meski Gemini error

## 🎯 Best Practices

### Untuk Dataset FAQ
1. **Tambah Paraphrases**: Semakin banyak variasi pertanyaan, semakin akurat
2. **Answer Variants**: Berikan beberapa variasi jawaban untuk respons yang natural
3. **Regular Update**: Update dataset berdasarkan pertanyaan yang sering masuk

### Untuk Gemini Integration
1. **Prompt Engineering**: Customize prompt untuk persona "JobMate Assistant"
2. **Context Provision**: Selalu berikan konteks dari database untuk konsistensi
3. **Error Handling**: Implementasikan fallback yang baik untuk error cases


## 🔗 API Documentation

**Live API**: https://faq-jobmate-api-705829099986.asia-southeast2.run.app

**Status**: 🟢 Online

**AI Features**: 
- 🤖 IndoBERT Semantic Search
- 🧠 Google Gemini AI Integration
- 🎯 Hybrid Response System

---

> **Note**: Pastikan `GOOGLE_API_KEY` sudah dikonfigurasi untuk mendapatkan pengalaman chat yang optimal dengan AI generative responses.

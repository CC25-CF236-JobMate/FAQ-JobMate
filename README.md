# JobMate FAQ Chatbot API

JobMate FAQ Chatbot adalah sistem chatbot berbasis AI yang menggunakan IndoBERT untuk memahami dan menjawab pertanyaan seputar pencarian kerja dalam bahasa Indonesia. Sistem ini menggunakan teknologi semantic similarity dengan FAISS indexing untuk memberikan jawaban yang akurat dan relevan.

## 🚀 Features

- **Semantic Search**: Menggunakan IndoBERT untuk memahami konteks pertanyaan
- **Fast Retrieval**: FAISS indexing untuk pencarian jawaban yang cepat
- **Multiple Answer Variants**: Mendukung variasi jawaban untuk respons yang lebih natural
- **Question Paraphrasing**: Dapat memahami berbagai cara bertanya yang sama
- **RESTful API**: Interface yang mudah diintegrasikan
- **Health Check**: Endpoint untuk monitoring status sistem
- **CORS Support**: Mendukung akses dari berbagai domain

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  IndoBERT Model  │───▶│ FAISS Index     │
│                 │    │  (Tokenization   │    │ (Similarity     │
│                 │    │   & Embedding)   │    │  Search)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                          │
┌─────────────────┐    ┌──────────────────┐              │
│ Response with   │◀───│  Answer Selection│◀─────────────┘
│ Confidence      │    │  & Confidence    │
│ Score           │    │  Calculation     │
└─────────────────┘    └──────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
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

4. **Prepare dataset**
   - Pastikan file `dataset/qnaJobMate.json` tersedia
   - Format dataset harus sesuai dengan struktur yang diharapkan

5. **Run application locally**
   ```bash
   python main.py
   ```

   Server akan berjalan di `http://localhost:8080`

## 📁 Project Structure

```
jobmate-faq-chatbot/
├── main.py                 # Aplikasi Flask utama
├── requirements.txt        # Dependencies Python
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

**Response:**
```json
{
  "answer": "Untuk mencari kerja yang efektif, Anda bisa...",
  "confidence": 0.92
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

1. **Build dan push image ke Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/capstone-jobseeker-dd654/faq-jobmate-api:latest
   ```

2. **Deploy ke Cloud Run**
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
     --memory 8Gi
   ```

3. **Live URL**
   ```
   https://faq-jobmate-api-705829099986.asia-southeast2.run.app
   ```

### Docker (Alternative)

```bash
# Build image
docker build -t jobmate-faq-api .

# Run container
docker run -p 8080:8080 jobmate-faq-api
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Port aplikasi |
| `HOST` | 0.0.0.0 | Host binding |

### Model Configuration

- **Model**: `indolem/indobert-base-uncased`
- **Max Length**: 64 tokens
- **Similarity Threshold**: 0.8
- **Top K Results**: 1

## 🧪 Testing

### Test API menggunakan curl

```bash
# Test FAQ endpoint
curl -X POST https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq \
  -H "Content-Type: application/json" \
  -d '{"question": "Daftar di JobMate Gimana"}'

# Test health check
curl https://faq-jobmate-api-705829099986.asia-southeast2.run.app/health
```

### Test menggunakan Python

```python
import requests

# Test FAQ
response = requests.post(
    'https://faq-jobmate-api-705829099986.asia-southeast2.run.app/faq',
    json={'question': 'Bisa Bookmark di JobMate'}
)
print(response.json())
```

## 🔧 Troubleshooting

### Common Issues

1. **Memory Error**
   - Pastikan container memiliki memory yang cukup (minimal 4GB)
   - Reduce batch size jika diperlukan

2. **Model Loading Timeout**
   - Increase timeout setting di Cloud Run
   - Use persistent storage untuk model caching

3. **Low Confidence Scores**
   - Review dan expand dataset FAQ
   - Adjust similarity threshold
   - Add more question paraphrases

## 📈 Performance Optimization

- **Model Caching**: Model dimuat sekali saat startup
- **Batch Processing**: Optimized untuk multiple queries
- **FAISS Indexing**: Fast similarity search
- **Normalized Embeddings**: Improved search accuracy

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

Project ini menggunakan MIT License. Lihat file `LICENSE` untuk detail lengkap.

## 👥 Team

- **Backend Developer**: [Your Name]
- **AI/ML Engineer**: [Your Name]
- **DevOps Engineer**: [Your Name]

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Check [Issues](link-to-issues) untuk masalah yang sudah diketahui
2. Buat issue baru dengan detail lengkap
3. Contact: [your-email@example.com]

---

**Live API**: https://faq-jobmate-api-705829099986.asia-southeast2.run.app

**Status**: 🟢 Online

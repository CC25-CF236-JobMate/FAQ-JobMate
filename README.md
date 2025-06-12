# JobMate FAQ Chatbot

A sophisticated, AI-powered chatbot designed to seamlessly answer frequently asked questions about the JobMate platform. This chatbot is built with a powerful natural language processing model to understand and respond to user queries in real-time, providing instant and accurate information.

**Live Demo Endpoint**: [https://faq-jobmate-api-705829099986.asia-southeast2.run.app](https://faq-jobmate-api-705829099986.asia-southeast2.run.app)

## Features

* **Natural Language Understanding**: Utilizes the `indolem/indobert-base-uncased` model to comprehend a wide range of questions formulated in natural Indonesian.
* **Instant & Accurate Responses**: Provides immediate and precise answers by leveraging a high-speed FAISS vector search to find the most relevant information from its knowledge base.
* **Paraphrase Handling**: Capable of understanding paraphrased questions, ensuring users get the right answer even if they don't use the exact official phrasing. The system is trained on a dataset containing original questions and their paraphrases.
* **Randomized Answers**: Delivers varied responses by randomly selecting from a list of answer paraphrases, making interactions feel more dynamic.
* **Simple API Interface**: Offers a straightforward API endpoint for easy integration with various front-end applications.
* **Health Check**: Includes a `/health` endpoint to monitor the operational status of the service.
* **Scalable Deployment**: Containerized with Docker, allowing for easy and scalable deployment on cloud platforms.

## Tech Stack

* **Backend**: Flask
* **ML/NLP**:
    * **`transformers`**: For leveraging the pre-trained IndoBERT model.
    * **`torch`**: As the core deep learning framework for the model.
    * **`faiss-cpu`**: For efficient similarity search in the vector space.
    * **`scikit-learn`**: For vector normalization.
    * **`numpy`**: For numerical operations.
* **Deployment**: Docker, Google Cloud Run
* **CORS Handling**: `Flask-Cors`

---

## How It Works

The system processes user queries through a multi-stage pipeline, from text preprocessing to returning a confident answer.

### 1. Model and Data Loading

At startup, the application loads the IndoBERT model and tokenizer. It also loads the `qnaJobMate.json` dataset, processing it into a flat list of all possible question variants and a corresponding list of potential answers.

```python
# main.py
# Load IndoBERT model & tokenizer once at startup
print("Loading IndoBERT model...")
model_name = "indolem/indobert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()
print("Model loaded.")

# Load and process the FAQ dataset
print("Loading and processing FAQ dataset...")
with open("dataset/qnaJobMate.json", "r", encoding="utf-8") as f:
    data = json.load(f)

all_questions = []
all_answers = []

for item in data:
    question_variants = [item['question']] + item.get('paraphrases', [])
    # ... (preprocessing)
    answer_variants = [item['answer']] + item.get('answer_paraphrases', [])
    for q in question_variants:
        all_questions.append(q)
        all_answers.append(answer_variants)
print("Dataset processed.")

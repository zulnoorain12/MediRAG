# 🩺 MediRAG — Intelligent Medical Assistant

> A safe, citation-backed medical chatbot powered by Retrieval-Augmented Generation (RAG), Google Gemini, and local HuggingFace embeddings.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3.1-1C3C3C?style=flat)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.3-orange?style=flat)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=flat&logo=google&logoColor=white)

---

## 📌 About the Project

**MediRAG** is an AI-powered medical assistant that answers health-related questions strictly from uploaded medical PDFs — eliminating hallucinations by using Retrieval-Augmented Generation (RAG). It combines a **FastAPI backend** with a multi-page **Streamlit frontend** to deliver a clean, professional medical Q&A experience with page-level source citations.

---

## ✨ Key Features

- 🔍 **No Hallucinations** — Answers are grounded strictly in your uploaded PDF documents
- 📄 **Page-Level Source Citations** — Every answer shows exactly which page/document it came from
- 🤗 **Local HuggingFace Embeddings** — Uses `all-MiniLM-L6-v2` offline; no embedding API quota needed
- 🧠 **Google Gemini LLM** — Powered by Gemini for high-quality, medically-aware responses
- ⚠️ **Safety Disclaimer** — Every response ends with *"Please consult a qualified doctor"*
- 💬 **Greeting Handling** — Detects small talk and responds naturally, not with RAG
- 📊 **Analytics & Feedback Page** — View usage stats and submit feedback
- 🗂️ **Multi-Page Streamlit UI** — Home, Chatbot, Upload, Analytics, About

---

## 🏗️ Project Architecture

```
MediRAG/
├── app.py                          # Streamlit home page
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (NOT on GitHub)
├── .gitignore
│
├── api/                            # FastAPI Backend
│   ├── main.py                     # FastAPI app entry point
│   ├── requirements-api.txt
│   ├── core/
│   │   ├── config.py               # Settings & environment config
│   │   └── rag_engine.py           # RAG chain with ChromaDB + Gemini
│   ├── routers/
│   │   └── chat.py                 # /api/v1/chat endpoint
│   ├── schemas/
│   │   └── chat.py                 # Pydantic request/response models
│   └── dependencies/
│       └── auth.py                 # Auth dependencies
│
├── pages/                          # Streamlit multi-page UI
│   ├── 1_Chatbot.py                # Chat interface
│   ├── 2_Upload_Documents.py       # PDF upload & indexing
│   ├── 3_Analytics_&_Feedback.py   # Usage analytics
│   └── 4_About.py                  # About page
│
├── utils/                          # Shared utilities
│   ├── document_processor.py       # PDF parsing & chunking
│   ├── logger.py                   # Loguru logging setup
│   ├── navbar.py                   # Custom sidebar navigation
│   ├── rag_chain.py                # RAG chain helpers
│   └── safety_filters.py           # Safety filter logic
│
└── data/                           # Local data (NOT on GitHub)
    ├── raw_docs/                   # Uploaded PDF files
    └── vector_db/                  # ChromaDB vector database
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.38.0 |
| **Backend** | FastAPI 0.115.0 + Uvicorn |
| **LLM** | Google Gemini (`langchain-google-genai`) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (local, offline) |
| **Vector Store** | ChromaDB |
| **Orchestration** | LangChain 0.3.1 |
| **PDF Parsing** | PyPDF |
| **Logging** | Loguru |
| **Environment** | python-dotenv |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository
```bash
git clone https://github.com/zulnoorain12/MediRAG.git
cd MediRAG
```

### 2. Create a Virtual Environment
```bash
python -m venv medrag_env

# Activate (Windows)
.\medrag_env\Scripts\activate

# Activate (Mac/Linux)
source medrag_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```
> ⚠️ **Never commit your `.env` file to GitHub.** It is already listed in `.gitignore`.

---

## 🚀 Running the Application

You need to run **two services** simultaneously — the FastAPI backend and the Streamlit frontend.

### Terminal 1 — Start the FastAPI Backend
```bash
uvicorn api.main:app --reload --port 8000
```
API will be available at: `http://127.0.0.1:8000`
Interactive API docs: `http://127.0.0.1:8000/docs`

### Terminal 2 — Start the Streamlit Frontend
```bash
streamlit run app.py
```
App will open at: `http://localhost:8501`

---

## 📖 How to Use

1. **Go to "Upload Documents"** — Upload one or more medical PDF files. The system will parse and index them into ChromaDB.
2. **Go to "Chatbot"** — Ask any medical question. The assistant retrieves relevant chunks from your PDFs and generates a cited answer.
3. **View sources** — Each response shows the source document and page number.
4. **Analytics** — View query history and submit feedback on the Analytics page.

---

## 🔒 Important Notes on Excluded Files

| Item | Status | Reason |
|---|---|---|
| `.env` (API keys) | ❌ Not on GitHub | Contains secret API keys — add manually |
| `medrag_env/` (virtual env) | ❌ Not on GitHub | Machine-specific — recreate with `pip install -r requirements.txt` |
| `data/` (vector DB + PDFs) | ❌ Not on GitHub | Generated at runtime when you upload documents |

---

## 🧪 Original Contributions (Beyond Standard RAG)

- ✅ **Local HuggingFace Embeddings** — Offline, unlimited, no API quota consumption
- ✅ **Page-Level Source Citations** — Pinpoints exact page numbers per answer
- ✅ **Greeting / Small Talk Handling** — Smart routing that avoids RAG for non-medical queries
- ✅ **Dedicated FastAPI Backend** — Decoupled API layer for scalability and extensibility
- ✅ **Multi-Page Streamlit UI** — Professional interface with custom navigation bar

---

## 🤝 Developers

Built as part of an academic project exploring Retrieval-Augmented Generation in the medical domain.

---

## ⚠️ Disclaimer

MediRAG is an **educational tool only**. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare professional for medical decisions.

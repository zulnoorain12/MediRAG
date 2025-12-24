# MediRAG: Medical Assistant with RAG, Memory & Safety
**A safe, citation-backed medical chatbot**

### Key Features
- No hallucinations (RAG from uploaded PDFs)
- Source citations with page numbers(in case of a multi paged PDF)
- Local HuggingFace embeddings (no quota)
- Multi-page UI (Upload + Chat)

### Original Contributions (Beyond Syllabus)
- Used **local HuggingFace embeddings** for unlimited, offline indexing
- Implemented **page-level source citations**
- Added **greeting handling** for better UX

### Tech Stack
- LangChain • ChromaDB • Gemini • HuggingFace • Streamlit

### Run
pip install -r requirements.txt

uvicorn api.main:app --reload --port 8000

streamlit run app.py

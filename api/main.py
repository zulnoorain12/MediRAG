# api/main.py - reloaded with gemini-3.5-flash-lite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat
from .core.config import settings
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MediRAG — Medical RAG API with source citation"
)

# Allow Streamlit frontend to talk to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod: ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "MediRAG API is running! Go to /docs for Swagger UI"}
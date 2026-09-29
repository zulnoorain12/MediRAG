# api/routers/chat.py
from fastapi import APIRouter, HTTPException
from ..schemas.chat import ChatRequest, ChatResponse, Source
from ..core.rag_engine import get_chain

from ..core.config import settings

router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.get("/health")
async def health():
    return {"status": "healthy", "model": settings.MODEL_NAME}

import os
import traceback

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        result = get_chain().invoke({"input": request.question})
        raw_answer = result.get("answer", "")
        
        # Ensure answer is always clean text (handles lists of ContentBlocks if returned by Gemini)
        if isinstance(raw_answer, list):
            parts = []
            for item in raw_answer:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
                else:
                    parts.append(str(item))
            answer = "".join(parts).strip()
        else:
            answer = str(raw_answer).strip()

        # Deduplicate sources
        sources = []
        seen_texts = set()
        for doc in result.get("context", []):
            snippet = doc.page_content[:200].strip()
            if snippet in seen_texts:
                continue
            seen_texts.add(snippet)
            filename = os.path.basename(doc.metadata.get("source", "Unknown"))
            sources.append(
                Source(
                    file=filename,
                    page=doc.metadata.get("page"),
                    text=doc.page_content[:250] + "..." if len(doc.page_content) > 250 else doc.page_content
                )
            )

        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
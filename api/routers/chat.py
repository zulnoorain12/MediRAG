# api/routers/chat.py
from fastapi import APIRouter, HTTPException
from ..schemas.chat import ChatRequest, ChatResponse, Source
from ..core.rag_engine import get_chain

router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.get("/health")
async def health():
    return {"status": "healthy", "model": "gemini-2.5-flash"}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = get_chain().invoke({"input": request.question})
        sources = [
            Source(
                file=doc.metadata.get("source", "Unknown").split("/")[-1],
                page=doc.metadata.get("page"),
                text=doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            )
            for doc in result.get("context", [])
        ]
        return ChatResponse(answer=result["answer"], sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
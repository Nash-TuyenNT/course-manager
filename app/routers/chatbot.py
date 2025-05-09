from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot.agent import agent_executor

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("/", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    result = agent_executor.invoke({"input": req.message})
    return ChatResponse(reply=result["output"])

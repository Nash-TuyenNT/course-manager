from typing import List

from fastapi import APIRouter
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.schemas.chat import ChatRequest, ChatResponse, Message
from app.services.chatbot.agent import ask_bot

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    chat_history: List[BaseMessage] = []

    for msg in req.history:
        if msg.sender == "human":
            chat_history.append(HumanMessage(content=msg.content))
        else:
            chat_history.append(AIMessage(content=msg.content))

    output, updated_history = ask_bot(req.input, chat_history)

    response_history = []
    for msg in updated_history:
        if isinstance(msg, HumanMessage):
            response_history.append(Message(sender="human", content=msg.content))
        elif isinstance(msg, AIMessage):
            response_history.append(Message(sender="ai", content=msg.content))

    return ChatResponse(output=output, history=response_history)

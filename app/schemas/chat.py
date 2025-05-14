from typing import Literal, List

from pydantic import BaseModel

class Message(BaseModel):
    sender: Literal["human", "ai"]
    content: str

class ChatRequest(BaseModel):
    input: str
    history: List[Message] = []

class ChatResponse(BaseModel):
    output: str
    history: List[Message]

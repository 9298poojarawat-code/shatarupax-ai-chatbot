from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=8000)


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=4000)
    history: List[HistoryMessage] = Field(default_factory=list, max_length=20)

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be empty")
        return value


class ChatResponse(BaseModel):
    response: str
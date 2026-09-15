from pydantic import BaseModel, field_validator


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Message khaali nahi ho sakta.")
        return value.strip()


class ChatResponse(BaseModel):
    response: str
    
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(max_length=300)


class MessageResponse(BaseModel):
    id: str
    username: str
    content: str
    timestamp: str

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Schema for a chat message request."""
    document_id: int = Field(..., description="ID of the document for the chat context.")
    message: str = Field(..., description="The user's chat message.")

class ChatResponse(BaseModel):
    """Schema for a chat message response."""
    response: str = Field(..., description="The AI's response to the user's message.")
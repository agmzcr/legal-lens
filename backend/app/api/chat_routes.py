"""
AI Chat Endpoint Module

Defines an API route that allows authenticated users to ask questions 
about a legal document using an AI-powered assistant.
"""

from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.auth.deps import get_current_user
from app.services.ai_engine import ask_ai_about_document
from app.models.user import User

# Initialize the router
router = APIRouter()

@router.post("/ai/chat")
def chat_with_ai(
    payload: dict = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Interacts with the AI to analyze and answer questions based on a document context.

    Parameters:
    - payload (dict): Should include 'context' (document text) and 'question' (user's query)
    - current_user (User): Automatically injected authenticated user

    Returns:
    - dict: Contains AI-generated 'answer' string
    """
    # Extract document text and user question from payload
    text = payload.get("context", "")
    question = payload.get("question", "")

    # Validate input
    if not text or not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'context' and 'question' fields are required."
        )

    # Generate response using AI engine
    answer = ask_ai_about_document(text, question)

    return {"answer": answer}
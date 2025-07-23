"""
AI Engine Module

Provides utility functions to interact with OpenRouter's AI API.
Includes:
- Document analysis (summary, clauses, red flags)
- Question answering based on document context
"""

import os
import json
import httpx
from dotenv import load_dotenv
from app.schemas.analysis import DocumentAnalysis, Clause

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "mistralai/mistral-7b-instruct:free"

def build_prompt(text: str) -> str:
    """
    Constructs an instruction prompt for document analysis.

    Args:
        text (str): Raw document content

    Returns:
        str: AI-friendly instruction prompt
    """
    return f"""
You are a legal assistant AI. Analyze the following legal document and return:
1. A short executive summary (max 5 lines).
2. A list of key clauses (title and short explanation).
3. A list of any potential red flags or legal risks.

Document:
\"\"\"
{text}
\"\"\"

Respond in JSON format with keys: summary, clauses (list of objects with title/content), red_flags (list of strings).
"""

def analyze_text_with_ai(text: str) -> DocumentAnalysis:
    """
    Sends document text to the AI model for legal analysis.

    Args:
        text (str): Full legal document content

    Returns:
        DocumentAnalysis: Parsed summary, clauses, and red flags
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Custom domain for tracing
        "X-Title": "LegalLens"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": build_prompt(text)}]
    }

    try:
        response = httpx.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)

        return DocumentAnalysis(
            summary=parsed.get("summary", ""),
            clauses=[
                Clause(title=cl.get("title", ""), content=cl.get("content", ""))
                for cl in parsed.get("clauses", [])
            ],
            red_flags=parsed.get("red_flags", [])
        )

    except Exception as e:
        print("Error communicating with OpenRouter:", e)
        return DocumentAnalysis(
            summary="Error analyzing document.",
            clauses=[],
            red_flags=["AI request failed."]
        )

def ask_ai_about_document(text: str, question: str) -> str:
    """
    Submits a question about a document to the AI model.

    Args:
        text (str): Full document context
        question (str): User’s legal question

    Returns:
        str: AI-generated answer or fallback message
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "LegalLens"
    }

    prompt = f"""
You are a legal assistant AI.

Document:
\"\"\"
{text}
\"\"\"

Question:
\"\"\"
{question}
\"\"\"

Answer the user's question clearly and precisely, based on the document above. Maximum 10 lines.
"""

    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = httpx.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("Error during AI chat:", e)
        return "Sorry, I couldn't process your question at this time."
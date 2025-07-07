import os
import httpx
from dotenv import load_dotenv
from app.schemas.analysis import DocumentAnalysis, Clause

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat"
LLM_MODEL = "mistral/mistral-7b-instruct"

def build_prompt(text: str) -> str:
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
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Can be anything for dev
        "X-Title": "LegalLens"
    }

    prompt = build_prompt(text)

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = httpx.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # Attempt to safely parse the response (assuming it returns valid JSON string)
        import json
        parsed = json.loads(content)

        return DocumentAnalysis(
            summary=parsed.get("summary", ""),
            clauses=[
                Clause(title=clause.get("title", ""), content=clause.get("content", ""))
                for clause in parsed.get("clauses", [])
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

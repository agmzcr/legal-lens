import json
import logging
import httpx

from app.config import settings
from app.schemas.document import DocumentSummary
from app.core.exceptions import AIEngineError

logger = logging.getLogger(__name__)

class AIEngineService:
    def __init__(self):
        self._api_key = settings.OPENROUTER_API_KEY
        self._base_url = settings.OPENROUTER_BASE_URL
        self._llm_model = settings.LLM_MODEL
        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",  # Custom domain for tracing
            "X-Title": "LegalLens"
        }

    def _send_request(self, messages: list[dict]) -> dict:
        """
        Sends a request to the OpenRouter API and handles potential errors.
        """
        payload = {
            "model": self._llm_model,
            "messages": messages
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(self._base_url, headers=self._headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP error with AI engine: {exc.response.status_code} - {exc.response.text}")
            raise AIEngineError(f"AI service returned an error: {exc.response.status_code}") from exc
        except httpx.RequestError as exc:
            logger.error(f"Network error communicating with AI engine: {exc}")
            raise AIEngineError("Network error connecting to AI service.") from exc
        except Exception as exc:
            logger.error(f"Unexpected error with AI engine request: {exc}")
            raise AIEngineError("An unexpected error occurred with the AI service.") from exc

    def analyze_text_with_ai(self, text: str) -> DocumentSummary:
        """
        Sends document text to the AI model for legal analysis.
        """
        prompt = f"""
        You are a legal assistant AI. Analyze the following legal document and return a JSON object with a summary, key clauses, and potential red flags.

        Document:
        \"\"\"
        {text}
        \"\"\"

        Respond in JSON format with keys: `summary` (string, max 5 lines), `clauses` (list of objects with `title` and `content`), and `red_flags` (list of strings).
        """
        messages = [{"role": "user", "content": prompt}]
        response_json = self._send_request(messages)
        content = response_json["choices"][0]["message"]["content"]
        
        try:
            parsed = json.loads(content)
            return {
                "summary": parsed.get("summary", ""),
                "clauses": parsed.get("clauses", []),
                "red_flags": parsed.get("red_flags", [])
            }
        except json.JSONDecodeError as exc:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            raise AIEngineError("The AI response could not be parsed.") from exc

    def get_ai_response(self, text: str, question: str) -> str:
        """
        Submits a question about a document to the AI model.
        """
        prompt = f"""
        You are a legal assistant AI. Answer the following question based only on the document provided. Do not use outside knowledge.

        Document:
        \"\"\"
        {text}
        \"\"\"

        Question:
        \"\"\"
        {question}
        \"\"\"

        Answer the user's question clearly and precisely. Maximum 10 lines.
        """
        messages = [{"role": "user", "content": prompt}]
        response_json = self._send_request(messages)
        return response_json["choices"][0]["message"]["content"]
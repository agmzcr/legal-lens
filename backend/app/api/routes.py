from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.document import Document
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ai_engine import analyze_text_with_ai
import json

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    content = await file.read()
    text = extract_text_from_pdf(content)
    analysis = analyze_text_with_ai(text)

    new_doc = Document(
        title=file.filename,
        content=text,
        summary=analysis.summary,
        red_flags=json.dumps(analysis.red_flags),
        user_id=current_user.id
    )
    session.add(new_doc)
    session.commit()

    return {
        "summary": analysis.summary,
        "clauses": [clause.dict() for clause in analysis.clauses],
        "red_flags": analysis.red_flags
    }

@router.get("/my-documents")
def get_my_documents(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    docs = session.exec(
        select(Document).where(Document.user_id == current_user.id)
    ).all()

    return [
        {
            "id": doc.id,
            "title": doc.title,
            "summary": doc.summary,
            "created_at": doc.created_at
        } for doc in docs
    ]

@router.delete("/document/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    doc = session.exec(
        select(Document).where(
            Document.id == doc_id,
            Document.user_id == current_user.id
        )
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or unauthorized")

    session.delete(doc)
    session.commit()
    return {"message": "Document deleted successfully"}

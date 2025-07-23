"""
Document Routes Module

Handles uploading, retrieving, listing, and deleting user documents.
Includes AI-powered parsing and analysis of PDF content.
"""

import json
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.document import Document
from app.services.pdf_parser import extract_text_from_pdf
from app.services.ai_engine import analyze_text_with_ai

# Initialize router
router = APIRouter()

@router.post("/document/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Uploads a PDF document, extracts its text, analyzes it using AI,
    and saves results in the database.

    Returns:
    - Document metadata and analysis summary
    """
    content = await file.read()
    text = extract_text_from_pdf(content)
    analysis = analyze_text_with_ai(text)

    new_doc = Document(
        title=file.filename,
        content=text,
        summary=analysis.summary,
        red_flags=json.dumps(analysis.red_flags),
        clauses=json.dumps([clause.dict() for clause in analysis.clauses]),
        user_id=current_user.id
    )
    session.add(new_doc)
    session.commit()

    return {
        "id": new_doc.id,
        "summary": analysis.summary,
        "clauses": [clause.dict() for clause in analysis.clauses],
        "red_flags": analysis.red_flags,
        "filename": file.filename
    }

@router.get("/document/{doc_id}")
def get_document_detail(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieves the full details of a specific document, ensuring it belongs to the current user.
    """
    doc = session.exec(
        select(Document).where(
            Document.id == doc_id,
            Document.user_id == current_user.id
        )
    ).first()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document not found or unauthorized"
        )

    return {
        "id": doc.id,
        "title": doc.title,
        "summary": doc.summary,
        "content": doc.content,
        "created_at": doc.created_at,
        "red_flags": json.loads(doc.red_flags or "[]"),
        "clauses": json.loads(doc.clauses or "[]")
    }

@router.get("/documents")
def get_documents(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Returns a list of all documents belonging to the current user.
    Includes basic metadata for display.
    """
    docs = session.exec(
        select(Document).where(Document.user_id == current_user.id)
    ).all()

    return [
        {
            "id": doc.id,
            "title": doc.title,
            "summary": doc.summary,
            "created_at": doc.created_at
        }
        for doc in docs
    ]

@router.delete("/document/{doc_id}")
def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Deletes a document if it belongs to the current user.
    """
    doc = session.exec(
        select(Document).where(
            Document.id == doc_id,
            Document.user_id == current_user.id
        )
    ).first()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Document not found or unauthorized"
        )

    session.delete(doc)
    session.commit()
    return {"message": "Document deleted successfully"}
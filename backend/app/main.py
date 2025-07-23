from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.document_routes import router as document_router
from app.api.auth_routes import router as auth_router
from app.api.chat_routes import router as chat_router
from app.db.init_db import init_db

app = FastAPI(
    title="LegalLens API",
    description="Analyze legal documents with AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)

@app.on_event("startup")
def on_startup():
    init_db()
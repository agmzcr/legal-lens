from fastapi import FastAPI
from app.api.routes import router as main_router
from app.api.auth_routes import router as auth_router
from app.db.init_db import init_db

app = FastAPI(
    title="LegalLens API",
    description="Analyze legal documents with AI",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(main_router)

@app.on_event("startup")
def on_startup():
    init_db()
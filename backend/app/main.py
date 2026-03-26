from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routes import auth, predict, history
from app.core.database import Base, engine
from app.models import HistoryEntry, User

app = FastAPI(title="Frouge API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(history.router)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/health")
def health():
    """Health check endpoint pour monitoring."""
    return {
        "status": "healthy",
        "service": "smartdrain-backend",
        "version": "1.0.0"
    }
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.history import HistoryCreate
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_history(db: Session = Depends(get_db)):
    return HistoryService.list_history(db)

@router.post("/")
def add_history(item: HistoryCreate, db: Session = Depends(get_db)):
    return HistoryService.add_history(db, item)
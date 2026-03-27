from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.history import HistoryCreate
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HistoryService.list_history(db, user_id=current_user.id)

@router.post("/")
def add_history(
    item: HistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HistoryService.add_history(db, item, user_id=current_user.id)
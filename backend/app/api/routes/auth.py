from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register(db=db, email=user.email, password=user.password)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login(db=db, email=user.email, password=user.password)

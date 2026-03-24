#route history
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

fake_users = {
    "demo@frouge.ai": "demo123",
    "test@frouge.ai": "test123",
}

class User(BaseModel):
    email: str
    password: str
@router.post("/register")
def register(user: User):
    if user.email in fake_users:
        raise HTTPException(status_code=400, detail="User already exists")

    fake_users[user.email] = user.password
    return {"message": "User created"}
@router.post("/login")
def login(user: User):
    if user.email not in fake_users or fake_users[user.email] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "token": "fake-jwt-token"}

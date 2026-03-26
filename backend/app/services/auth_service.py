import hashlib
import hmac
import os

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

_HASH_SALT = os.getenv("AUTH_SALT", "smartdrain-dev-salt")


class AuthService:
	@staticmethod
	def _hash_password(password: str) -> str:
		payload = f"{_HASH_SALT}:{password}".encode("utf-8")
		return hashlib.sha256(payload).hexdigest()

	@classmethod
	def register(cls, db: Session, email: str, password: str) -> dict:
		existing = db.query(User).filter(User.email == email).first()
		if existing:
			raise HTTPException(status_code=400, detail="User already exists")

		user = User(email=email, password_hash=cls._hash_password(password))
		db.add(user)
		db.commit()
		db.refresh(user)
		return {"message": "User created", "id": user.id, "email": user.email}

	@classmethod
	def login(cls, db: Session, email: str, password: str) -> dict:
		user = db.query(User).filter(User.email == email).first()
		if not user:
			raise HTTPException(status_code=401, detail="Invalid credentials")

		submitted_hash = cls._hash_password(password)
		if not hmac.compare_digest(user.password_hash, submitted_hash):
			raise HTTPException(status_code=401, detail="Invalid credentials")

		return {"message": "Login successful", "token": "fake-jwt-token"}
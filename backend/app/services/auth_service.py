import hashlib
import hmac
import os

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User

_HASH_SALT = os.getenv("AUTH_SALT", "smartdrain-dev-salt")
_TOKEN_SALT = os.getenv("TOKEN_SALT", "smartdrain-token-salt")


class AuthService:
	@staticmethod
	def _normalize_email(email: str) -> str:
		return email.strip().lower()

	@staticmethod
	def _token_signature(user_id: int) -> str:
		payload = f"{_TOKEN_SALT}:{user_id}".encode("utf-8")
		return hashlib.sha256(payload).hexdigest()

	@classmethod
	def create_access_token(cls, user_id: int) -> str:
		signature = cls._token_signature(user_id)
		return f"u.{user_id}.{signature}"

	@staticmethod
	def _hash_password(password: str) -> str:
		payload = f"{_HASH_SALT}:{password}".encode("utf-8")
		return hashlib.sha256(payload).hexdigest()

	@classmethod
	def register(cls, db: Session, email: str, password: str) -> dict:
		normalized_email = cls._normalize_email(email)
		existing = db.query(User).filter(func.lower(User.email) == normalized_email).first()
		if existing:
			raise HTTPException(status_code=400, detail="User already exists")

		user = User(email=normalized_email, password_hash=cls._hash_password(password))
		db.add(user)
		db.commit()
		db.refresh(user)
		return {"message": "User created", "id": user.id, "email": user.email}

	@classmethod
	def login(cls, db: Session, email: str, password: str) -> dict:
		normalized_email = cls._normalize_email(email)
		user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
		if not user:
			raise HTTPException(status_code=401, detail="Invalid credentials")

		submitted_hash = cls._hash_password(password)
		if not hmac.compare_digest(user.password_hash, submitted_hash):
			raise HTTPException(status_code=401, detail="Invalid credentials")

		return {"message": "Login successful", "token": cls.create_access_token(user.id)}

	@classmethod
	def get_user_from_token(cls, db: Session, token: str) -> User | None:
		parts = token.split(".")
		if len(parts) != 3 or parts[0] != "u":
			return None

		try:
			user_id = int(parts[1])
		except ValueError:
			return None

		expected_signature = cls._token_signature(user_id)
		if not hmac.compare_digest(parts[2], expected_signature):
			return None

		return db.query(User).filter(User.id == user_id).first()
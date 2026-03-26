from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class HistoryEntry(Base):
    __tablename__ = "history_entries"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    detection_count = Column(Integer, nullable=False, default=0)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

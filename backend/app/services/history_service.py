from sqlalchemy.orm import Session

from app.models.history import HistoryEntry
from app.schemas.history import HistoryCreate


class HistoryService:
	@staticmethod
	def list_history(db: Session) -> list[dict]:
		rows = db.query(HistoryEntry).order_by(HistoryEntry.created_at.desc()).all()
		return [
			{
				"id": row.id,
				"filename": row.filename,
				"timestamp": row.created_at,
				"status": row.status,
				"detectionCount": row.detection_count,
				"type": row.type,
			}
			for row in rows
		]

	@staticmethod
	def add_history(db: Session, item: HistoryCreate) -> dict:
		row = HistoryEntry(
			filename=item.filename,
			status=item.status,
			detection_count=item.detectionCount,
			type=item.type,
		)
		db.add(row)
		db.commit()
		db.refresh(row)
		return {
			"message": "Saved",
			"id": row.id,
		}
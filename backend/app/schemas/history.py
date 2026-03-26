from datetime import datetime

from pydantic import BaseModel


class HistoryCreate(BaseModel):
    filename: str
    status: str
    detectionCount: int
    type: str


class HistoryResponse(BaseModel):
    id: int
    filename: str
    timestamp: datetime
    status: str
    detectionCount: int
    type: str

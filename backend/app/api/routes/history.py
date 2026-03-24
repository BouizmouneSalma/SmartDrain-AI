from fastapi import APIRouter

router = APIRouter(prefix="/history", tags=["History"])

fake_history = [
    {
        "filename": "cover_001.jpg",
        "timestamp": "2026-03-23T10:15:00",
        "status": "Completed",
        "detectionCount": 3,
        "type": "Good",
    },
    {
        "filename": "cover_002.jpg",
        "timestamp": "2026-03-23T10:32:00",
        "status": "Completed",
        "detectionCount": 2,
        "type": "Broken",
    },
    {
        "filename": "cover_003.jpg",
        "timestamp": "2026-03-23T11:04:00",
        "status": "Completed",
        "detectionCount": 1,
        "type": "Lose",
    },
    {
        "filename": "cover_004.jpg",
        "timestamp": "2026-03-23T11:20:00",
        "status": "Completed",
        "detectionCount": 4,
        "type": "Good",
    },
]

@router.get("/")
def get_history():
    return fake_history

@router.post("/")
def add_history(item: dict):
    fake_history.append(item)
    return {"message": "Saved"}
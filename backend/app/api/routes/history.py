from fastapi import APIRouter

router = APIRouter(prefix="/history", tags=["History"])

fake_history = []

@router.get("/")
def get_history():
    return fake_history

@router.post("/")
def add_history(item: dict):
    fake_history.append(item)
    return {"message": "Saved"}
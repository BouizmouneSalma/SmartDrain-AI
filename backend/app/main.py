from fastapi import FastAPI

app = FastAPI(title="smartdrain-ai")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


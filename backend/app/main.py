from fastapi import FastAPI
from backend.app.api.routes import auth, predict, history

app = FastAPI(title="Frouge API")

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(history.router)

@app.get("/")
def root():
    return {"message": "API running"}
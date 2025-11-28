from fastapi import FastAPI 
from .api.workouts import router as workouts_router

app = FastAPI()


@app.get("/health")

def health_check():
    return {"status": "ok"}

app.include_router(workouts_router)

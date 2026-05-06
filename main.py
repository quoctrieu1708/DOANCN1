from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Face Recognition AI Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI Service is running"}

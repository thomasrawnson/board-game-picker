from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Board Game Picker API",
    description="Board game collection and recommendation API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Board Game Picker!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/api/message")
def get_message():
    return {
        "message": "Hello from the Board Game Picker API!"
    }
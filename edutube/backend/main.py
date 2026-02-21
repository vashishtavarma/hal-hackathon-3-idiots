# main.py
"""EduTube API — FastAPI application for learning journeys, chapters, notes, and chatbot."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_mongodb, close_mongodb
from app.routers import users, journeys, chapters, notes, chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_mongodb()
    yield
    await close_mongodb()


app = FastAPI(
    title="EduTube API",
    description="Learning journeys, chapters, notes, and chatbot.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes under /api/v1
app.include_router(users.router, prefix="/api/v1")
app.include_router(journeys.router, prefix="/api/v1")
app.include_router(chapters.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(chatbot.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "This api is working"}

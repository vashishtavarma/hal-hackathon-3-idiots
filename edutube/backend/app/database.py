# app/database.py
"""MongoDB connection and collection access."""

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from app.config import settings

# Global client and DB references (set at startup in connect_mongodb)
client: AsyncIOMotorClient | None = None
db: Any = None  # AsyncIOMotorDatabase after connect


def get_db() -> Any:
    """Return the current MongoDB database. Use this instead of importing db directly,
    so services always see the connected db after lifespan startup."""
    if db is None:
        raise RuntimeError("Database not initialized; connect_mongodb() has not run or failed.")
    return db


async def connect_mongodb() -> None:
    """Create MongoDB connection and ensure indexes."""
    global client, db  # noqa: PLW0603
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]  # type: ignore[assignment]

    # Indexes for common queries
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username")
    await db.journeys.create_index("user_id")
    await db.journeys.create_index([("is_public", ASCENDING)])
    await db.chapters.create_index("journey_id")
    await db.chapters.create_index([("journey_id", ASCENDING), ("chapter_no", ASCENDING)])
    await db.notes.create_index("chapter_id")
    await db.notes.create_index("journey_id")


async def close_mongodb() -> None:
    """Close MongoDB connection."""
    global client, db
    if client:
        client.close()
        client = None
    db = None

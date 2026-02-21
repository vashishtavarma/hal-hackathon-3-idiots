# app/services/user_service.py
"""User CRUD and auth logic using MongoDB."""

from bson import ObjectId

from app.database import get_db
from app.schemas import doc_to_user


async def create_user(username: str, email: str, password_hash: str) -> str:
    """Insert user; returns new id as string."""
    db = get_db()
    result = await db.users.insert_one(
        {"username": username, "email": email, "password": password_hash}
    )
    return str(result.inserted_id)


async def find_user_by_email(email: str) -> dict | None:
    """Return user doc (with _id) or None."""
    return await get_db().users.find_one({"email": email})


async def find_user_by_id(user_id: str) -> dict | None:
    """Return user doc or None. Raises if invalid ObjectId."""
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None
    doc = await get_db().users.find_one({"_id": oid})
    return doc


async def find_all_users() -> list[dict]:
    """Return all users as list of dicts with 'id' key."""
    cursor = get_db().users.find({})
    users = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        users.append(doc)
    return users

# app/services/journey_service.py
"""Journey CRUD and fork logic using MongoDB."""

from bson import ObjectId

from app.database import get_db
from app.schemas import doc_to_journey


def _oid(s: str) -> ObjectId | None:
    try:
        return ObjectId(s)
    except Exception:
        return None


async def create_journey(
    title: str,
    description: str,
    is_public: bool,
    user_id: str,
) -> str:
    db = get_db()
    uid = _oid(user_id)
    result = await db.journeys.insert_one(
        {
            "title": title or "Untitled Journey",
            "description": description or "",
            "is_public": is_public,
            "user_id": user_id,
        }
    )
    return str(result.inserted_id)


async def get_all_journeys(user_id: str) -> list[dict]:
    db = get_db()
    cursor = db.journeys.find({"user_id": user_id})
    out = []
    async for doc in cursor:
        out.append(doc_to_journey(doc))
    return out


async def get_journey_by_id(journey_id: str) -> dict | None:
    oid = _oid(journey_id)
    if not oid:
        return None
    doc = await get_db().journeys.find_one({"_id": oid})
    if not doc:
        return None
    return doc_to_journey(doc)


async def update_journey(
    journey_id: str,
    user_id: str,
    title: str | None,
    description: str | None,
    is_public: bool | None,
) -> bool:
    oid = _oid(journey_id)
    if not oid:
        return False
    update: dict = {}
    if title is not None:
        update["title"] = title
    if description is not None:
        update["description"] = description
    if is_public is not None:
        update["is_public"] = is_public
    if not update:
        return True
    r = await get_db().journeys.update_one(
        {"_id": oid, "user_id": user_id},
        {"$set": update},
    )
    return r.modified_count > 0


async def delete_journey(journey_id: str, user_id: str) -> bool:
    oid = _oid(journey_id)
    if not oid:
        return False
    r = await get_db().journeys.delete_one({"_id": oid, "user_id": user_id})
    return r.deleted_count > 0


async def get_all_public_journeys() -> list[dict]:
    """Return public journeys with username from users collection."""
    # user_id in journeys is stored as string; users._id is ObjectId
    cond = [
        {"$and": [{"$ne": ["$user_id", None]}, {"$ne": ["$user_id", ""]}]},
        {"$toObjectId": "$user_id"},
        None,
    ]
    pipeline = [
        {"$match": {"is_public": True}},
        {
            "$lookup": {
                "from": "users",
                "let": {"uid": {"$cond": cond}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$uid"]}}},
                    {"$project": {"username": 1}},
                ],
                "as": "user_doc",
            }
        },
        {"$unwind": {"path": "$user_doc", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "title": 1,
                "description": 1,
                "is_public": 1,
                "username": "$user_doc.username",
            }
        },
    ]
    db = get_db()
    out = []
    async for doc in db.journeys.aggregate(pipeline):
        if "_id" in doc:
            del doc["_id"]
        out.append(doc)
    return out


async def fork_journey(journey_id: str, user_id: str) -> str:
    """Copy journey, its chapters and notes for the user; returns new journey id."""
    journey = await get_journey_by_id(journey_id)
    if not journey:
        raise ValueError("Journey not found")

    new_title = f"Fork of {journey.get('title') or 'Untitled'}"
    new_jid = await create_journey(
        title=new_title,
        description=journey.get("description") or "",
        is_public=False,
        user_id=user_id,
    )
    new_oid = ObjectId(new_jid)
    db = get_db()

    # Copy chapters and build old_id -> new_id map
    old_to_new_chapter: dict[str, str] = {}
    async for ch in db.chapters.find({"journey_id": journey_id}):
        new_ch = await db.chapters.insert_one(
            {
                "title": ch.get("title") or "Untitled Chapter",
                "description": ch.get("description") or "",
                "video_link": ch.get("video_link") or "",
                "external_link": ch.get("external_link") or "",
                "is_completed": False,
                "chapter_no": ch.get("chapter_no", 1),
                "journey_id": new_jid,
            }
        )
        old_to_new_chapter[str(ch["_id"])] = str(new_ch.inserted_id)

    # Copy notes
    async for note in db.notes.find({"journey_id": journey_id}):
        old_ch_id = str(note.get("chapter_id") or "")
        new_ch_id = old_to_new_chapter.get(old_ch_id)
        if new_ch_id:
            await db.notes.insert_one(
                {
                    "content": note.get("content") or "",
                    "chapter_id": new_ch_id,
                    "journey_id": new_jid,
                }
            )

    return new_jid

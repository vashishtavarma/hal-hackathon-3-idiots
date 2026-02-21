# app/services/chapter_service.py
"""Chapter CRUD using MongoDB."""

from bson import ObjectId

from app.database import get_db
from app.schemas import doc_to_chapter


def _oid(s: str) -> ObjectId | None:
    try:
        return ObjectId(s)
    except Exception:
        return None


async def create_chapter(
    journey_id: str,
    title: str,
    description: str,
    video_link: str,
    external_link: str,
    chapter_no: int,
) -> str:
    db = get_db()
    result = await db.chapters.insert_one(
        {
            "title": title,
            "description": description or "",
            "video_link": video_link,
            "external_link": external_link or "",
            "is_completed": False,
            "chapter_no": chapter_no,
            "journey_id": journey_id,
        }
    )
    return str(result.inserted_id)


async def get_chapters_by_journey_id(journey_id: str) -> list[dict]:
    db = get_db()
    cursor = db.chapters.find({"journey_id": journey_id}).sort("chapter_no", 1)
    out = []
    async for doc in cursor:
        out.append(doc_to_chapter(doc))
    return out


async def get_chapter_by_id(chapter_id: str) -> dict | None:
    oid = _oid(chapter_id)
    if not oid:
        return None
    doc = await get_db().chapters.find_one({"_id": oid})
    if not doc:
        return None
    return doc_to_chapter(doc)


async def update_chapter(
    chapter_id: str,
    title: str | None,
    description: str | None,
    video_link: str | None,
    external_link: str | None,
    chapter_no: int | None,
) -> bool:
    oid = _oid(chapter_id)
    if not oid:
        return False
    update: dict = {}
    if title is not None:
        update["title"] = title
    if description is not None:
        update["description"] = description
    if video_link is not None:
        update["video_link"] = video_link
    if external_link is not None:
        update["external_link"] = external_link
    if chapter_no is not None:
        update["chapter_no"] = chapter_no
    if not update:
        return True
    r = await get_db().chapters.update_one({"_id": oid}, {"$set": update})
    return r.modified_count > 0


async def update_chapter_complete(chapter_id: str, is_completed: bool) -> bool:
    oid = _oid(chapter_id)
    if not oid:
        return False
    r = await get_db().chapters.update_one(
        {"_id": oid},
        {"$set": {"is_completed": is_completed}},
    )
    return r.modified_count > 0


async def delete_chapter(chapter_id: str) -> bool:
    oid = _oid(chapter_id)
    if not oid:
        return False
    r = await get_db().chapters.delete_one({"_id": oid})
    return r.deleted_count > 0

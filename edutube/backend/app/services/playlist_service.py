# app/services/playlist_service.py
"""YouTube playlist fetch for journey-from-playlist feature."""

import httpx

from app.config import settings

YT_KEY = settings.yt_key or ""


async def get_playlist_details(playlist_id: str) -> tuple[str, str]:
    """Return (title, description) for the playlist. Uses mock data if no API key."""
    if not YT_KEY or "demo" in YT_KEY:
        return f"Playlist {playlist_id}", f"Demo playlist description for {playlist_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://www.googleapis.com/youtube/v3/playlists",
            params={"part": "snippet", "id": playlist_id, "key": YT_KEY},
        )
        r.raise_for_status()
        data = r.json()
    if not data.get("items"):
        raise ValueError("Playlist not found")
    snippet = data["items"][0]["snippet"]
    return snippet.get("title", ""), snippet.get("description", "")


async def get_playlist_videos(playlist_id: str) -> list[dict]:
    """Return list of {title, videoLink, description, chapterNo}. Uses mock if no API key."""
    if not YT_KEY or "demo" in YT_KEY:
        return [
            {
                "title": "Introduction to the Course",
                "videoLink": "https://www.youtube.com/watch?v=Tn6-PIqc4UM",
                "description": "First chapter introducing basic concepts.",
                "chapterNo": 1,
            },
            {
                "title": "Advanced Topics",
                "videoLink": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "description": "Deep dive into advanced topics.",
                "chapterNo": 2,
            },
        ]

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            params={
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": 50,
                "key": YT_KEY,
            },
        )
        r.raise_for_status()
        data = r.json()
    if not data.get("items"):
        raise ValueError("No videos found in playlist")

    out = []
    for i, item in enumerate(data["items"]):
        snippet = item.get("snippet", {})
        desc = (snippet.get("description") or "")[:150]
        if len((snippet.get("description") or "")) > 150:
            last_space = desc.rfind(" ")
            desc = (desc[: last_space] + "...") if last_space > 0 else desc + "..."
        video_id = snippet.get("resourceId", {}).get("videoId", "")
        out.append(
            {
                "title": snippet.get("title") or f"Chapter {i + 1}",
                "videoLink": f"https://www.youtube.com/watch?v={video_id}" if video_id else "no video",
                "description": desc,
                "chapterNo": i + 1,
            }
        )
    return out

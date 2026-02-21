# app/routers/users.py
"""User registration, login, profile, and list."""

import bcrypt
from fastapi import APIRouter, HTTPException, status

from app.auth import create_access_token, get_current_user, CurrentUser
from app.schemas import (
    UserRegister,
    UserCreateResponse,
    UserLogin,
    TokenResponse,
    UserResponse,
)
from app.services.user_service import (
    create_user,
    find_user_by_email,
    find_user_by_id,
    find_all_users,
)

router = APIRouter(prefix="/users", tags=["users"])

# Bcrypt truncates at 72 bytes; hash password as utf-8 bytes for consistency
def _hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


@router.post("/register", response_model=UserCreateResponse)
async def register(body: UserRegister):
    """Register a new user. Returns { id }."""
    existing = await find_user_by_email(body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    hashed = _hash_password(body.password)
    user_id = await create_user(body.username, body.email, hashed)
    return UserCreateResponse(id=user_id)


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin):
    """Login; returns { token }."""
    user = await find_user_by_email(body.email)
    if not user or not _verify_password(body.password, user.get("password", "")):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(
        {"id": str(user["_id"]), "username": user["username"], "email": user["email"]}
    )
    return TokenResponse(token=token)


@router.get("/profile", response_model=UserResponse)
async def get_profile(user: CurrentUser):
    """Return current user profile { id, username, email }."""
    uid = user.get("id")
    doc = await find_user_by_id(uid)
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=str(doc["_id"]), username=doc["username"], email=doc["email"])


@router.get("")
async def get_users():
    """Return all users (list of { id, username, email, ... })."""
    users = await find_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

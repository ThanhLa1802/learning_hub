from fastapi import APIRouter, Cookie, HTTPException, Response, status
from jose import JWTError
import uuid

from app.api.v1.deps import SessionDep
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.repositories import user as user_crud
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse

router = APIRouter()

COOKIE_MAX_AGE_ACCESS = 30 * 60          # 30 minutes
COOKIE_MAX_AGE_REFRESH = 7 * 24 * 60 * 60  # 7 days


def _set_auth_cookies(response: Response, user_id: str) -> str:
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax", max_age=COOKIE_MAX_AGE_ACCESS, secure=False)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax", max_age=COOKIE_MAX_AGE_REFRESH, secure=False)
    return access_token


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, response: Response, session: SessionDep):
    if user_crud.get_by_email(session, request.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = user_crud.create(session, request.email, hash_password(request.password), request.full_name)
    _set_auth_cookies(response, str(user.id))
    return user


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, response: Response, session: SessionDep):
    user = user_crud.get_by_email(session, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    access_token = _set_auth_cookies(response, str(user.id))
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(response: Response, session: SessionDep, refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user_id = uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = user_crud.get_by_id(session, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = _set_auth_cookies(response, str(user.id))
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

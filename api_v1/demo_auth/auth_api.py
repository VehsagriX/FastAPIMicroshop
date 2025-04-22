import secrets
import uuid
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["demo-auth"])
security = HTTPBasic()

"""
Basic auth
"""


@router.get("/basic-auth")
def basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


username_to_passwords = {
    "admin": "admin",
    "john": "john123",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    # secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc
    return credentials.username


@router.get("/basic-auth-username")
def basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi {auth_username}",
        "username": auth_username,
    }


"""
Headers auth
"""
static_auth_token_to_username = {
    "89d7731e9bbc34e8e46a08b3be1a17d": "admin",
    "ab1e915c48555c2036763ceb8cb24407a": "john",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return static_auth_token_to_username[static_token]


@router.get("/http-header-auth")
def demo_http_header_auth(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi {username}",
        "username": username,
    }


"""
Cookie auth
"""
COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return COOKIES[session_id]


@router.post("/login-cookie")
def demo_auth_login_set_cookie(
    response: Response,
    username: str = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": datetime.now(),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    return {"message": f"Hello{username}", **user_session_data}


@router.get("/logout-cookie")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id, None)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"message": f"Bye {username}"}

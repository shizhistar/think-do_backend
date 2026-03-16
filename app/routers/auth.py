"""
认证相关接口：注册、登录、当前用户。
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.auth import create_access_token, get_current_user
from app.db.crud import create_user, get_user_by_email, verify_password
from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
def register(
    body: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    """
    注册新用户。邮箱不可重复。
    成功返回 JWT access_token，前端后续请求在 Header 中带：Authorization: Bearer <token>。
    """
    if get_user_by_email(db, body.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )
    user = create_user(
        db,
        email=body.email,
        password=body.password,
        name=body.name,
    )
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    """
    邮箱 + 密码登录。成功返回 JWT access_token。
    """
    user = get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
        )
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    """
    获取当前登录用户信息。需要在 Header 中携带：Authorization: Bearer <access_token>。
    """
    return UserResponse.model_validate(user)

"""
JWT 生成、校验及「当前用户」依赖，用于登录态与接口鉴权。
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.db.models import User
from app.db.crud import get_user_by_id

# Bearer Token 方案
security = HTTPBearer(auto_error=False)


def create_access_token(subject: str | int) -> str:
    """根据用户标识（如 user_id）生成 JWT access token。"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(subject), "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """解码 JWT，成功返回 sub（通常为 user_id），失败返回 None。"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


def get_current_user_optional(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> User | None:
    """
    可选当前用户：有合法 Bearer token 则返回 User，否则返回 None。
    用于「登录可选」的接口。
    """
    if not credentials:
        return None
    user_id_str = decode_access_token(credentials.credentials)
    if not user_id_str:
        return None
    try:
        user_id = int(user_id_str)
    except ValueError:
        return None
    return get_user_by_id(db, user_id)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> User:
    """
    必须登录：无 token 或 token 无效时返回 401。
    用于需要登录才能访问的接口。
    """
    user = get_current_user_optional(db, credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

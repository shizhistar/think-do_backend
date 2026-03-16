"""
登录、注册相关的请求与响应模型。
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """注册请求：邮箱、密码、可选昵称。"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128, description="密码 6～128 位")
    name: str | None = Field(None, max_length=255)


class LoginRequest(BaseModel):
    """登录请求：邮箱 + 密码。"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """登录/注册成功返回：access_token 与类型。"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """对外返回的用户信息（不含密码）。"""
    id: int
    email: str
    name: str | None
    intro: str | None

    class Config:
        from_attributes = True

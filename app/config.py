"""
应用配置：MySQL 连接串、JWT 密钥、大模型 API Key 等。
从环境变量读取，建议用 .env 管理。
"""
# # try:
from pydantic_settings import BaseSettings  # type: ignore[import-untyped]
# # except ImportError:
# from pydantic import BaseSettings  # pydantic v1


class Settings(BaseSettings):
    # 开发时设为 True 可在 500 响应中看到具体错误信息
    DEBUG: bool = False

    # 数据库（charset=utf8mb4 支持中文等 4 字节字符）
    MYSQL_URL: str = "mysql+pymysql://root:password@localhost:3306/softs_db?charset=utf8mb4"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天

    # 大模型（后续接 API 时用）
    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

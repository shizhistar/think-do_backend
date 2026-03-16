"""
数据库基础设施：engine、SessionLocal、Base、get_db。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# 确保连接使用 utf8mb4，否则中文等字符会报 Incorrect string value
mysql_url = settings.MYSQL_URL
if "charset=" not in mysql_url:
    mysql_url += "&charset=utf8mb4" if "?" in mysql_url else "?charset=utf8mb4"

engine = create_engine(
    mysql_url,
    pool_pre_ping=True,  # 使用前检测连接是否有效
    echo=False,         # 设为 True 可打印每条 SQL，便于调试
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类"""
    pass


def get_db():
    """依赖注入用：每个请求一个 session，用完后关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

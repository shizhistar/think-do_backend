"""
SQLAlchemy 模型：User、Personality。
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


# 简介最大字数（按需可改）
INTRO_MAX_LENGTH = 500


# 建表时使用 utf8mb4，避免中文等字符报 Incorrect string value
_UTF8MB4_TABLE_ARGS = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}


class User(Base):
    __tablename__ = "users"
    __table_args__ = _UTF8MB4_TABLE_ARGS

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)   # 不唯一
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)   # 密码哈希，不存明文
    intro = Column(String(INTRO_MAX_LENGTH), nullable=True)   # 简介，限制字数
    personality = relationship("Personality", back_populates="user", uselist=False)


class Personality(Base):
    __tablename__ = "personalities"
    __table_args__ = _UTF8MB4_TABLE_ARGS

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)   # 外键且为主键，一对一
    diet = Column(String(512), nullable=True)      # 饮食喜好
    travel = Column(String(512), nullable=True)   # 旅游喜好
    dressing = Column(String(512), nullable=True) # 穿搭喜好
    overall = Column(String(512), nullable=True)  # 总体喜好

    user = relationship("User", back_populates="personality")

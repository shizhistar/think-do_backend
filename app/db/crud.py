"""
数据库增删改查，供 API 层调用，不直接写 SQL。
"""
import bcrypt
from sqlalchemy.orm import Session

from app.db.models import User, Personality

# bcrypt 限制密码最多 72 字节
BCRYPT_MAX_PASSWORD_BYTES = 72


def _hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:BCRYPT_MAX_PASSWORD_BYTES]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:BCRYPT_MAX_PASSWORD_BYTES],
            password_hash.encode("utf-8"),
        )
    except Exception:
        return False


# ---------- User ----------
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    email: str,
    password: str,
    name: str | None = None,
    intro: str | None = None,
) -> User:
    user = User(
        email=email,
        password_hash=_hash_password(password),
        name=name,
        intro=intro,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    user_id: int,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    intro: str | None = None,
) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if password is not None:
        user.password_hash = _hash_password(password)
    if intro is not None:
        user.intro = intro[:500] if len(intro) > 500 else intro  # 遵守简介字数限制
    db.commit()
    db.refresh(user)
    return user


# ---------- Personality ----------
def get_personality_by_user_id(db: Session, user_id: int) -> Personality | None:
    return db.query(Personality).filter(Personality.user_id == user_id).first()


def create_or_update_personality(
    db: Session,
    user_id: int,
    diet: str | None = None,
    travel: str | None = None,
    dressing: str | None = None,
    overall: str | None = None,
) -> Personality:
    p = get_personality_by_user_id(db, user_id)
    if p:
        if diet is not None:
            p.diet = diet
        if travel is not None:
            p.travel = travel
        if dressing is not None:
            p.dressing = dressing
        if overall is not None:
            p.overall = overall
        db.commit()
        db.refresh(p)
        return p
    p = Personality(
        user_id=user_id,
        diet=diet,
        travel=travel,
        dressing=dressing,
        overall=overall,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.db.database import Base, engine
import app.db.models  # 必须导入，表才会注册到 Base.metadata
from app.routers import auth


async def catch_all_exception_handler(request: Request, exc: Exception):
    """开发时返回 500 的具体错误信息，便于排查"""
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(exc)},
        )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


def _ensure_utf8mb4(engine):
    """把当前库和已存在的表转为 utf8mb4，解决已有表字符集不对导致中文报错的问题"""
    from sqlalchemy import text
    try:
        db_name = engine.url.database
        with engine.connect() as conn:
            try:
                conn.execute(text(f"ALTER DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
            except Exception:
                conn.rollback()
            for table in ("users", "personalities"):
                try:
                    conn.execute(text(f"ALTER TABLE `{table}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                    conn.commit()
                except Exception:
                    conn.rollback()
    except Exception:
        pass  # 权限不足等不影响启动，新表仍会按 __table_args__ 用 utf8mb4


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时建表（仅开发/演示用；生产建议用 Alembic 做迁移）
    Base.metadata.create_all(bind=engine)
    _ensure_utf8mb4(engine)
    yield
    # 关闭时如需可释放连接池
    engine.dispose()


app = FastAPI(title="Mobile Backend", lifespan=lifespan)
app.add_exception_handler(Exception, catch_all_exception_handler)

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
"""数据库连接（日8第一刀：先连上 MySQL）。

TODO 你来填：
1) 从环境变量读 DATABASE_URL
2) create_engine(...)
3) SessionLocal = sessionmaker(...)
4) class Base(DeclarativeBase)
5) def get_db(): yield session（给 FastAPI 依赖用）
"""

from __future__ import annotations

# TODO: imports
# TODO: engine / SessionLocal / Base / get_db
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
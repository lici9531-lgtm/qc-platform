"""测试前后自动建表 / 删表（Day15 测试隔离）。

跑测试时 DATABASE_URL 要指向 qc_platform_test，别指向正式库！
"""

import pytest

from app.db import Base, engine
import app.models  # noqa: F401  让 Base 认识所有表


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    if not engine.url.database.endswith("_test") :
        raise RuntimeError("DATABASE_URL 要指向 qc_platform_test，别指向正式库！")
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
        

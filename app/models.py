"""ORM：两张表的说明书（对应数据库里的 datasets / runs）。

先看教练讲义里「每一列干什么」，再取消注释并补全。
不要抄完整答案——按列自己写。
"""

from __future__ import annotations

# TODO: from datetime import datetime
# TODO: from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
# TODO: from sqlalchemy.orm import Mapped, mapped_column, relationship
# TODO: from app.db import Base
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# class Dataset(Base):
#     __tablename__ = "datasets"
#     id: ...
#     name: ...              # 人能看懂的名字，可选
#     file_path: ...         # CSV 落盘路径
#     created_at: ...
class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)



# class Run(Base):
#     __tablename__ = "runs"
#     id: ...
#     dataset_id: ...        # 外键 → datasets.id
#     status: ...            # queued|running|succeeded|failed
#     error: ...             # 失败原因，如 interrupted；成功可为 null
#     report_json: ...       # 成功后的报告全文（先简单存 Text）
#     rules_version: ...
#     input_sha256: ...
#     created_at: ...
#     finished_at: ...       # 结束时间；未结束可为 null
class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dataset_id: Mapped[int] = mapped_column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(200), nullable=False,index=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    report_json: Mapped[str | None] = mapped_column(LONGTEXT, nullable=True)
    rules_version: Mapped[str] = mapped_column(String(64), nullable=True)
    input_sha256: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

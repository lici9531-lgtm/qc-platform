"""接口进出的 JSON 形状（Pydantic）。日8稍后填；先占位。"""

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from pydantic import field_validator




class DatasetCreate(BaseModel):
    name: str | None = None
    file_path: str

class DatasetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str | None
    file_path: str
    created_at: datetime
    @field_validator("created_at")
    @classmethod
    def mark_utc(cls, v: datetime | None) -> datetime | None:
        if v is None:
            return None
        return v.replace(tzinfo=timezone.utc)

class RunCreate(BaseModel):
    dataset_id: int

class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    dataset_id: int
    status: str
    error: str | None
    created_at: datetime
    finished_at: datetime | None
    rules_version: str | None = None
    input_sha256: str | None = None
    @field_validator("created_at", "finished_at")
    @classmethod
    def mark_utc(cls, v: datetime | None) -> datetime | None:
        if v is None:
            return None
        return v.replace(tzinfo=timezone.utc)

class RunListOut(BaseModel):
    items: list[RunOut]
    total: int
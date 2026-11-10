"""FastAPI 入口。五接口 + 同步质检状态机。"""

from __future__ import annotations

import json
import os,time
import logging

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy import func , select
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app import cache
from app.models import Dataset, Run
from app.qc_engine import run_qc
from app.schemas import DatasetCreate, DatasetOut, RunCreate, RunOut,RunListOut
from app.models import utc_now

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        stuck = db.scalars(
            select(Run).where(Run.status.in_(["queued", "running"]))
        ).all()
        for row in stuck:
            old = row.status
            row.status = "failed"
            row.error = "interrupted: service restarted before run finished"
            row.finished_at = utc_now()
            logger.warning("run_id=%s dataset_id=%s from=%s to=%s error=%s", row.id,row.dataset_id,old,row.status,row.error)
        db.commit()
        logger.warning("recovered count=%s",len(stuck))
    yield
app = FastAPI(title="qc-platform", version="0.1.0",lifespan=lifespan)

logging.basicConfig(
    level = os.getenv("LOG_LEVEL", "INFO"),
    format = "%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

    


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/datasets", response_model=DatasetOut)
def create_dataset(
    payload: DatasetCreate,
    db: Session = Depends(get_db),
):
    row = Dataset(
        name=payload.name,
        file_path=payload.file_path,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.post("/runs", response_model=RunOut)
def create_run(payload: RunCreate, db: Session = Depends(get_db)):
    dataset = db.get(Dataset, payload.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="dataset not found")

    # 开单
    row = Run(dataset_id=payload.dataset_id, status="queued")
    db.add(row)
    db.commit()
    db.refresh(row)
    logger.info("run_id=%s dataset_id=%s status=%s",row.id,payload.dataset_id,"queued")
    # 开始跑
    row.status = "running"
    db.commit()
    logger.info("run_id=%s status=%s",row.id,"running")
    try:
        slow = int(os.getenv("QC_DEMO_SLEEP", "0"))
        if slow:
            time.sleep(slow)
        report = run_qc(dataset.file_path)
        row.report_json = json.dumps(report, ensure_ascii=False)
        row.rules_version = report.get("rules_version")
        row.input_sha256 = report.get("input_sha256")

        if report.get("error"):
            # 质检函数认出了问题（如文件不存在）
            row.status = "failed"
            row.error = report["error"]
            logger.error("run_id=%s status=%s error=%s",row.id,"failed",row.error)
        else:
            row.status = "succeeded"
            row.error = None
            logger.info("run_id=%s status=%s",row.id,"succeeded")

        row.finished_at = utc_now()
    except Exception as e:
        # 没预料到的崩溃
        row.status = "failed"
        row.error = str(e)
        row.finished_at = utc_now()
        logger.error("run_id=%s status=%s error=%s",row.id,"failed",row.error)

    db.commit()

    # 报告刚落库：主动失效（谁改数据谁清缓存）。删失败只记日志，不能让成功的工单变失败。
    #   注意位置：必须是 db.commit() 之后——先落库，再清缓存，顺序反了会留下旧值
    cache.delete_cached_report(row.id)

    db.refresh(row)
    return row


@app.get("/runs", response_model=RunListOut)
def list_runs(status : Literal["queued", "running", "succeeded", "failed"] | None = None,order : Literal["asc", "desc"] = Query("asc"),dataset_id:int | None = None,limit: int = Query( 10, ge=1,le=50),offset:int = Query(0,ge=0), db: Session = Depends(get_db)):
    stmt = select(Run)
    if status is not None:
        stmt = stmt.where(Run.status == status)
    if dataset_id is not None:
        stmt = stmt.where(Run.dataset_id == dataset_id)
    
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    if order =="asc":
        stmt = stmt.order_by(Run.id).limit(limit).offset(offset)
    else:
        stmt = stmt.order_by(Run.id.desc()).limit(limit).offset(offset)
    rows = db.scalars(stmt).all()
    return {"items": rows, "total": total}


@app.get("/runs/{run_id}", response_model=RunOut)
def get_run(run_id: int, db: Session = Depends(get_db)):
    row = db.get(Run, run_id)
    if not row:
        raise HTTPException(status_code=404, detail="run not found")
    return row


@app.get("/runs/{run_id}/report")
def get_run_report(run_id: int, db: Session = Depends(get_db)):
    # ---- ① 先问缓存 ----
    cached = cache.get_cached_report(run_id)
    if cached is not None:
        logger.info("run_id=%s report_cache=hit", run_id)
        return json.loads(cached)
    logger.info("run_id=%s report_cache=miss", run_id)

    # ---- ② 未命中 / 缓存挂了：回源查库 ----
    row = db.get(Run, run_id)
    if not row:
        raise HTTPException(status_code=404, detail="run not found")
    if row.status != "succeeded" or not row.report_json:
        raise HTTPException(status_code=409, detail="report not ready")

    # ---- ③ 查到报告：写回缓存再返回 ----
    cache.set_cached_report(run_id, row.report_json)
    # 注意：404 / 409 这两条分支绝不能写缓存

    return json.loads(row.report_json)

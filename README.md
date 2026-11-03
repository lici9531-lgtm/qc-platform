# qc-platform — 数据质检与实验分析平台（运维向）

一句话：用 FastAPI + MySQL 提供数据集与质检 run 的同步执行 API，经 Docker Compose 一键复现。

> **Stub 状态**：当前 `Dockerfile` / `api` 为最小 HTTP stub，便于 Compose 拉起与运维演练；业务接口待后端接入后替换。密钥与 venv 永不入库。

## 前置

- Git
- Docker Engine + Docker Compose v2（`docker compose version`）

## 快速开始（可复现）

```bash
git clone <仓库地址> qc-platform
cd qc-platform
cp .env.example .env          # 按需改假值；勿提交真实 .env
docker compose up --build -d  # 一次拉起 db + api
docker compose ps             # 确认 db healthy、api 运行中
```

健康检查 / curl 示例（**接口待后端就绪**；stub 仅返回占位 JSON）：

```bash
curl -s http://127.0.0.1:8000/
# 待后端接入后示例：
# curl -s -X POST http://127.0.0.1:8000/datasets -H 'Content-Type: application/json' -d '{...}'
# curl -s -X POST http://127.0.0.1:8000/runs -H 'Content-Type: application/json' -d '{...}'
# curl -s http://127.0.0.1:8000/runs
# curl -s http://127.0.0.1:8000/runs/{id}
# curl -s http://127.0.0.1:8000/runs/{id}/report
```

停止（保留数据）：

```bash
docker compose down
```

## 本地开发（可选）

venv **不入库**。可连 Compose 里的 MySQL：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 确保 docker compose up -d db 已起，且 .env 中 MYSQL_HOST=127.0.0.1（本机连映射端口）
# 待后端接入: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 目录说明

```
qc-platform/
├── app/                 # 应用代码（待后端接入）
├── db/                  # init_db.sql 等（待后端接入）
├── sql/                 # schema / queries（待后端接入）
├── tests/               # pytest（待后端接入）
├── docs/                # 部署手册、演练记录、已知限制、运行步骤、环境变量、Git 规范
├── Dockerfile           # 当前 stub；待后端接入后换真实 CMD
├── docker-compose.yml   # db + api 一次拉起
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

目标 API（章程，待后端接入）：`POST /datasets`、`POST /runs`、`GET /runs`、`GET /runs/{id}`、`GET /runs/{id}/report`。

## 重启与数据

| 项 | 说明 |
|----|------|
| Volume 名 | `qc-platform-mysql-data`（compose 中 `mysql_data`） |
| 重启服务 | `docker compose restart` 或 `docker compose up -d` |
| 数据不丢口径 | `docker compose down`（不加 `-v`）后再次 `up`，MySQL 数据仍在命名 volume |
| 慎用 | `docker compose down -v` 会删除 volume，数据丢失 |

## 中断恢复口径

- 执行模型：单 worker **同步**执行；状态机 `queued → running → succeeded | failed`
- 启动时扫描卡在 `running` / `queued` 的僵尸 run，标为 `failed`（`error=interrupted`）
- **不自动重跑**
- 细则见 [docs/部署与故障手册.md](docs/部署与故障手册.md)

## 环境变量

见 [.env.example](.env.example) 与 [docs/环境变量清单.md](docs/环境变量清单.md)。真实 `.env` 永不提交。

## 已知限制

见 [docs/已知限制.md](docs/已知限制.md)。日常命令见 [docs/运行步骤.md](docs/运行步骤.md)。故障演练模板见 [docs/故障演练记录.md](docs/故障演练记录.md)。

## Git

见 [docs/Git规范.md](docs/Git规范.md)。禁止提交：`.env`、venv、密钥、本地 uploads。

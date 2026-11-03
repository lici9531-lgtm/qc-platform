# qc-platform API 镜像
# 安装 requirements.txt 后以 uvicorn 启动 app.main:app（端口 8000）。
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 先装依赖，利于层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=100 -r requirements.txt

# 拷贝应用（后端落地后 app/ 会有真实代码；现仅有 .gitkeep）
COPY app/ ./app/
COPY .env.example ./.env.example

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Git 规范（本地 / 协作）

## 分支

- 主分支建议：`main`（或团队约定的 `master`，保持单一主线）
- 功能分支：`feat/<简述>`、`fix/<简述>`、`ops/<简述>`
- 合入主分支前自行 rebase/merge，保持历史可读

## Commit 信息建议

```
<type>: <简述>

类型示例：feat / fix / docs / ops / chore / test
```

示例：`ops: 补充 compose 健康检查与演练模板`

## 禁止提交

- **`.env` 及真实密钥**（只允许 `.env.example`）
- **venv / `.venv`**
- `__pycache__`、`.pytest_cache`、覆盖率 HTML、IDE 配置（见 `.gitignore`）
- 本地 `uploads/`、数据文件、`*.sql.gz` 备份
- 含密码的 `docker-compose.override.yml`（若使用）

红线：**密钥与 venv 永不入库**。提交前自查：`git status`、`git diff`。

## Tag 约定（E2）

- 里程碑发布打 tag：`v1.0`（及后续 `v1.x`）
- 建议附简短 message：`git tag -a v1.0 -m "E2: compose 可复现与运维手册"`
- 验收口述：干净 clone + `docker compose up`；重启不丢数据；中断恢复有日志证据

## 本仓库初始化提示

若本地尚未 `git init`：可按需初始化；**不要**添加含密钥的 remote 凭据文件；**不要** commit `.env`。远程 URL 由团队另行配置。

# app/cache.py —— Redis 缓存层（骨架，待实现）
#
# 目标：给报告接口提供「取缓存 / 写缓存 / 删缓存」三个小函数，
#       并且保证【缓存出故障不会让接口出故障】。
#
# 你需要在下面填空。每填一块，先在心里回答该块上方的问号。

import logging
import os

import redis


# ---------------------------------------------------------------
# 1. 客户端（模块级只建一次）
#
#    ? 为什么放模块级，而不是每个请求新建？
#    ? decode_responses=True 解决的是什么问题？
#    ? host 从哪来？为什么不写死 "localhost"？
# ---------------------------------------------------------------

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "")

# URL 为空就不建客户端：模块导入不能因为缓存没配好就崩掉整个应用
client = redis.Redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None

# ---------------------------------------------------------------
# 2. TTL 从环境变量读，给默认值
#
#    ? 读出来是字符串还是整数？ clues: int(...)
# ---------------------------------------------------------------

REPORT_CACHE_TTL = int(os.getenv("REPORT_CACHE_TTL", "600"))


# ---------------------------------------------------------------
# 3. 缓存键
#
#    ? 为什么是 report:{run_id} 而不是 dataset:{id}？
#    ? 返回的是 str 还是 bytes？
# ---------------------------------------------------------------

def report_key(run_id: int) -> str:
    """把 run_id 转成缓存键。"""
    return f"report:{run_id}"



# ---------------------------------------------------------------
# 4. 读缓存 —— 失败必须降级成「未命中」
#
#    ? 未命中时该返回什么？（提示：redis 客户端取不到 key 返回 None）
#    ? Redis 连不上抛的异常，应该吞掉还是往外抛？为什么？
#    ? 吞掉之前必须做的一件事是什么？（提示：不然你永远不知道缓存挂了）
# ---------------------------------------------------------------

def get_cached_report(run_id: int):
    """返回缓存的报告字符串；未命中或出错一律返回 None。"""
    if client is None:
        return None
    try:
        key = report_key(run_id)
        return client.get(key)
    except Exception as e:
        logger.warning("run_id=%s cache_get_failed err=%s", run_id, e)
        return None


# ---------------------------------------------------------------
# 5. 写缓存 —— 失败只记日志，绝不 raise
#
#    ? 为什么这里不能抛异常？（提示：报告已经查到了，接口该不该因为它 500？）
#    ? TTL 是硬编码 600 好，还是从 REPORT_CACHE_TTL 读好？
# ---------------------------------------------------------------

def set_cached_report(run_id: int, report_json: str) -> None:
    """把报告写进缓存，带 TTL。失败只记日志。"""
    if client is None:
        return
    key = report_key(run_id)
    try:
        client.set(key, report_json, ex=REPORT_CACHE_TTL)
    except Exception as e:
        logger.warning("run_id=%s cache_set_failed err=%s", run_id, e)


# ---------------------------------------------------------------
# 6. 删缓存 —— 数据变了就调它
#
#    ? 删一个不存在的 key 会报错吗？
#    ? 失败能不能 raise？（提示：工单已经成功了）
# ---------------------------------------------------------------

def delete_cached_report(run_id: int) -> None:
    """删掉某次 run 的报告缓存。失败只记日志。"""
    if client is None:
        return
    key = report_key(run_id)
    try:
        client.delete(key)
    except Exception as e:
        logger.warning("run_id=%s cache_delete_failed err=%s", run_id, e)


# ---------------------------------------------------------------
# 7.（可选）健康检查
#
#    给 /health 或启动日志用：redis 连不上时不要让进程起不来，
#    只打印一行警告——这是「缓存是附加件」的体现。
# ---------------------------------------------------------------

def cache_ping() -> bool:
    """Redis 可用返回 True，否则 False（不抛异常）。"""
    if client is None:
        return False
    try:
        client.ping()
        return True
    except Exception as e:
        logger.warning("cache_ping failed err=%s", e)
        return False

from functools import lru_cache
from typing import Optional

from ip_api_py import IPInfoApi, IPInfoDt

api = IPInfoApi(
    fields=[
        "query",
        "status",
        "continent",
        "country",
        "countryCode",
        "region",
        "regionName",
        "city",
        "isp",
        "query",
        "lat",
        "lon",
    ],
    lang="zh-CN",
    timeout_seconds=5,
    wait_seconds=3,
)

__all__ = ["get_ip_info"]


@lru_cache(maxsize=64 * 1024)  # add lru cache to prevent hit rate limit
def get_ip_info(ip: str) -> Optional[IPInfoDt]:
    return api.get_ip_info(ip)

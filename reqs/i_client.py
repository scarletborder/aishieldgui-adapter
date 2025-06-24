import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aiohttp
from typing import Dict, Any, Optional
from dataclasses import dataclass
from models.url_options import URLOptions
from models.file_options import FileOptions


@dataclass
class APIResponse:
    code: int
    msg: str
    data: Optional[Dict[str, Any]] = None


class IAPIClient:
    """
    APIClient的接口定义，提供基本的API请求方法。
    具体实现类需要实现这些方法。
    """

    async def __aenter__(self):
        """进入异步上下文管理器"""
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出异步上下文管理器"""
        raise NotImplementedError

    async def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> APIResponse:
        """发送API请求"""
        raise NotImplementedError

    async def update_status(self, uuid: str, status: str, message: str) -> None:
        """更新项目状态"""
        raise NotImplementedError

    async def update_progress(self, uuid: str, progress: int, message: str) -> None:
        """更新项目进度"""
        raise NotImplementedError

    async def submit_result(self, uuid: str, result: list[dict]) -> None:
        """提交检测结果"""
        raise NotImplementedError

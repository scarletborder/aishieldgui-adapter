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


class APIClient:
    """
    一个 APIClient 的模拟版本 (Mock Version)。
    它包含所有与原始类相同的方法，但不执行任何实际的网络请求。
    所有的网络操作都被替换为控制台打印语句，以模拟其行为。
    """

    def __init__(self, base_url: str = "http://localhost:3000/projects"):
        self.base_url = base_url.rstrip("/")
        # 不再需要 aiohttp session
        print(f"--- MockAPIClient 初始化 ---")
        print(f"   - 模拟目标 Base URL: {self.base_url}")

    async def __aenter__(self):
        # 模拟进入异步上下文管理器
        print("\n[CONTEXT] ==> 进入 MockAPIClient 上下文管理器...")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 模拟退出异步上下文管理器
        print("[CONTEXT] <== 退出 MockAPIClient 上下文管理器.")

    async def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> APIResponse:
        # 模拟内部请求方法
        url = f"{self.base_url}/api/v1{endpoint}"
        print("\n" + "=" * 50)
        print("--- 模拟内部请求 (_make_request) ---")
        print(f"  - 方法 (Method): {method}")
        print(f"  - 终点 (Endpoint): {url}")
        print(f"  - 数据 (Data): {data}")
        print("=" * 50)

        # 返回一个模拟的、成功的 APIResponse
        return APIResponse(
            code=200,
            msg="OK (Mocked Response)",
            data={"success": True, "mock_data": "This is a mock response."},
        )

    async def update_status(self, uuid: str, status: str, message: str) -> None:
        # 模拟更新状态
        print(f"\n🟢 [状态更新] 🟢")
        print(f"  - UUID: {uuid}")
        print(f"  - 新状态: {status}")
        print(f"  - 消息: {message}")
        print(f"  - 模拟请求: POST {self.base_url}/status")

    async def update_progress(self, uuid: str, progress: int, message: str) -> None:
        # 模拟更新进度
        progress_bar = f"[{'#' * (progress // 10):<10}]"
        print(f"\n📊 [进度更新] 📊")
        print(f"  - UUID: {uuid}")
        print(f"  - 进度: {progress}% {progress_bar}")
        print(f"  - 消息: {message}")
        print(f"  - 模拟请求: POST {self.base_url}/progress")

    async def submit_result(self, uuid: str, result: Any) -> None:
        # 模拟提交结果
        print(f"\n✨ [结果提交] ✨")
        print(f"  - UUID: {uuid}")
        print(f"  - 提交内容: {result}")
        print(f"  - 模拟请求: POST {self.base_url}/result")

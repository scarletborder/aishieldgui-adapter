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
    def __init__(self, base_url: str = "http://localhost:3000/projects"):
        self.base_url = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> APIResponse:
        if not self.session:
            raise RuntimeError(
                "Client session not initialized. Use 'async with' context manager."
            )

        url = f"{self.base_url}/api/v1{endpoint}"
        async with self.session.request(method, url, json=data) as response:
            result = await response.json()
            return APIResponse(
                code=result.get("code", -1),
                msg=result.get("msg", ""),
                data=result.get("data"),
            )

    async def update_status(self, uuid: str, status: str, message: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/status",
                json={"status": status, "message": message},
            ) as response:
                response.raise_for_status()

    async def update_progress(self, uuid: str, progress: int, message: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/progress",
                json={"progress": progress, "message": message},
            ) as response:

                response.raise_for_status()

    async def submit_result(self, uuid: str, result: Any) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/result",
                json=result,
            ) as response:
                response.raise_for_status()

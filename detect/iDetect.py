from abc import ABC, abstractmethod
from typing import Any
from models.i_options import IOptions
from reqs.i_client import IAPIClient


class IDetect(ABC):
    """检测接口基类"""

    @abstractmethod
    async def run(self, options: IOptions, api_client: IAPIClient) -> None:
        """运行检测

        Args:
            options: 检测选项
            api_client: API客户端实例

        Returns:
            检测结果
        """
        pass

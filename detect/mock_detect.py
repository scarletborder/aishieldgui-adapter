import sys
import os
import subprocess
import json

from models.i_options import IOptions
from reqs.i_client import IAPIClient
from utils.corepath import GetPlmDefenseDefensePath, GetProtoShieldConfigPath

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import Any

from logic.logic import GenerateResult
from detect.iDetect import IDetect
from models.url_options import URLOptions
from reqs.api_client import APIClient
from models.result import ResultItem


class MockDetect(IDetect):
    """URL检测实现"""

    # 防御方法与config文件的映射
    DEFENSE_METHOD_MAP = {
        "MODELDEFENSETYPEONION": "Badnets4OnlyONIONConfig.json",
        "MODELDEFENSETYPECUBE": "Badnets4OnlyCUBEConfig.json",
        "MODELDEFENSETYPESTRIP": "Badnets4OnlySTRIPConfig.json",
        "MODELDEFENSETYPEPROTO_SHIELD": "Badnets4GA+LoRA+MSLRConfig.json",
    }

    async def run(self, options: IOptions, api_client: IAPIClient) -> None:
        """运行URL检测

        Args:
            options: URL检测选项
            api_client: API客户端实例

        Returns:
            检测结果
        """
        if not isinstance(options, IOptions):
            raise TypeError("options must be IOptions")

        if not options.validate():
            raise ValueError("Invalid options")

        try:
            # 更新状态为checking
            await api_client.update_status(options.uuid, "checking", "开始检测")

            results: list[dict] = []
            for method in options.defense_methods:
                # 模拟检测过程
                total_steps = 100
                for step in range(0, total_steps, 8):
                    # 更新进度
                    progress = int((step + 1) / total_steps * 100)
                    await api_client.update_progress(
                        options.uuid, progress, f"正在检测... {progress}%"
                    )
                    await asyncio.sleep(0.2)  # 模拟处理时间

                # 提交结果
                result = await GenerateResult()
                results.append({"method": method, "result": result})
            await api_client.update_status(options.uuid, "completed", "检测完成")
            await api_client.submit_result(options.uuid, results)
            # return result.to_dict()

        except Exception as e:
            await api_client.update_status(
                options.uuid, "completed", f"检测失败: {str(e)}"
            )
            raise

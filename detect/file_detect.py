import sys
import os
import subprocess
import json

from reqs.i_client import IAPIClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import Any

from logic.logic import GenerateResult
from detect.iDetect import IDetect
from models.file_options import FileOptions
from reqs.api_client import APIClient
from models.result import ResultItem
from utils.corepath import GetPlmDefenseDefensePath, GetProtoShieldConfigPath


class FileDetect(IDetect):
    """文件检测实现"""

    # 防御方法与config文件的映射
    DEFENSE_METHOD_MAP = {
        "MODELDEFENSETYPEONION": "Badnets4OnlyONIONConfig.json",
        "MODELDEFENSETYPECUBE": "Badnets4OnlyCUBEConfig.json",
        "MODELDEFENSETYPESTRIP": "Badnets4OnlySTRIPConfig.json",
        "MODELDEFENSETYPEPROTO_SHIELD": "Badnets4GA+LoRA+MSLRConfig.json",
    }

    async def run(self, options: FileOptions, api_client: IAPIClient) -> None:
        """运行文件检测

        Args:
            options: 文件检测选项
            api_client: API客户端实例

        Returns:
            检测结果
        """
        if not isinstance(options, FileOptions):
            raise TypeError("options must be FileOptions")

        if not options.validate():
            raise ValueError("Invalid options")

        try:
            # 更新状态为checking
            await api_client.update_status(options.uuid, "checking", "开始检测file")

            results = []
            for method in options.defense_methods:
                config_file = self.DEFENSE_METHOD_MAP.get(method)
                if not config_file:
                    continue
                config_path = GetProtoShieldConfigPath(config_file)
                plm_defense_path = GetPlmDefenseDefensePath()
                cmd = [sys.executable, plm_defense_path, "--config_path", config_path]
                # 可根据options补充参数，如--target_model, --dataset, --poison_rate
                if options.local_file:
                    cmd += ["--target_model", options.local_file]
                    cmd += ["--model_source", "local"]
                if hasattr(options, "dataset") and options.dataset:
                    cmd += ["--dataset", options.dataset]
                if hasattr(options, "poison_rate") and options.poison_rate:
                    cmd += ["--poison_rate", str(options.poison_rate)]

                # 2. 启动子进程并实时读取进度
                process = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                progress = 0
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8").strip()
                    # 你可以在plmDefense.py里加print(f"PROGRESS:{percent}")来配合解析
                    if decoded.startswith("PROGRESS:"):
                        try:
                            progress = int(decoded.split(":")[1])
                            await api_client.update_progress(
                                options.uuid,
                                progress,
                                f"[{method}] 正在检测... {progress}%",
                            )
                        except Exception:
                            pass
                await process.wait()
                # 3. 读取检测结果（假设plmDefense.py最后输出json结果）
                # 这里假设结果保存在某个json文件里
                result_path = os.path.join(
                    os.path.dirname(config_path), "last_result.json"
                )
                if os.path.exists(result_path):
                    with open(result_path, "r", encoding="utf-8") as f:
                        result_data = json.load(f)
                    result = ResultItem.from_dict(result_data)
                else:
                    result = ResultItem(Uuid=options.uuid, ModelStatus="error")
                results.append({"method": method, "result": result.to_dict()})
            await api_client.update_status(options.uuid, "completed", "检测完成")
            await api_client.submit_result(options.uuid, results)
            # return results

        except Exception as e:
            # 发生错误时更新状态
            await api_client.update_status(
                options.uuid, "completed", f"检测失败: {str(e)}"
            )
            raise

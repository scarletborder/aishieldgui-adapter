# 实际上url和file都是将模型文件进行检测
# 这里是主入口

import sys
import os



from models.result import ResultItem
from models.url_options import URLOptions
from models.file_options import FileOptions
from reqs.api_client import APIClient

import json
import random
from pathlib import Path


async def Run(options: FileOptions, api_client: APIClient) -> ResultItem:
    result = await GenerateResult()
    return result


# 生成结果
async def GenerateResult() -> ResultItem:
    # example, 从文件中随机生成结果
    # 当前运行的python脚本文件的目录 + examples 下的随机一个json
    # 然后读取json文件, 随机生成结果

    # 获取当前运行的脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # 构建examples目录路径
    examples_dir = os.path.join(current_dir, "examples")

    # 获取所有json文件
    json_files = list(Path(examples_dir).glob("*.json"))

    if not json_files:
        raise FileNotFoundError("在examples目录下未找到任何json文件")

    # 随机选择一个json文件
    random_file = random.choice(json_files)

    # 读取并解析json文件
    with open(random_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    return result

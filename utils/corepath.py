"""
获取core路径

例如检测代码的路径
"""
import json
from pathlib import Path
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 全局变量
ProtoShieldPath: str = ""


def GetCoreDirPath() -> str:
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def GetExampleDirPath() -> str:
    return os.path.join(GetCoreDirPath(), "examples")


def GetRandomExampleJsonPath() -> str:
    examples_dir = GetExampleDirPath()

    json_files = list(Path(examples_dir).glob("*.json"))
    if not json_files:
        raise FileNotFoundError("在examples目录下未找到任何json文件")

    # 随机选择一个json文件
    random_file = random.choice(json_files)

    # 读取并解析json文件
    with open(random_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    return result


def InitProtoShieldPath(protoShieldPath: str) -> str:
    # 根据cmd传入path进行初始化
    global ProtoShieldPath
    ProtoShieldPath = protoShieldPath


def GetProtoShieldDirPath() -> str:
    return ProtoShieldPath


def GetProtoShieldConfigPath(
    fileName: str = "plmConfigs/Badnets4GA+LoRA+MSLRConfig.json",
) -> str:
    return os.path.join(GetProtoShieldDirPath(), fileName)


def GetPlmDefenseDefensePath() -> str:
    return os.path.join(GetProtoShieldDirPath(), "plmDefense.py")

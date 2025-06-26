#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import asyncio
import sys
import os

from reqs.mock_client import MockClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detect.mock_detect import MockDetect
from utils.corepath import InitProtoShieldPath
from models.url_options import URLOptions
from models.file_options import FileOptions
from detect.url_detect import URLDetect
from detect.file_detect import FileDetect
from reqs.api_client import APIClient


def parse_args():
    parser = argparse.ArgumentParser(description="AI模型防御工具")

    # 必选参数
    parser.add_argument(
        "--uuid", required=True, help="项目的唯一标识符，由GUI生成并传递"
    )
    parser.add_argument(
        "--model-type",
        required=True,
        choices=["QWEN", "LLAMA", "BERT"],
        help="模型类型，必须是指定的三种之一",
    )

    # 模型来源参数（二选一）
    model_source = parser.add_mutually_exclusive_group(required=True)
    model_source.add_argument(
        "--url",
        help="Hugging Face模型URL，例如 https://huggingface.co/meta-llama/Llama-2-7b-chat-hf",
    )
    model_source.add_argument(
        "--local-file", help="本地模型文件路径，支持 *.bin, *.pth, *.pt 等格式"
    )

    # 防御方法参数
    parser.add_argument(
        "--defense-methods",
        nargs="+",
        required=True,
        choices=[
            "MODELDEFENSETYPEONION",
            "MODELDEFENSETYPECUBE",
            "MODELDEFENSETYPESTRIP",
            "MODELDEFENSETYPEPROTO_SHIELD",
        ],
        help="防御方法列表，可多选",
    )

    # 持久化配置中的参数
    parser.add_argument("--proto-shield-path", required=True, help="ProtoShield路径")
    parser.add_argument("--detect-mode", required=True, help="检测模式: app / exp")
    parser.add_argument("--posion-rate", required=False, help="中毒率")

    parser.add_argument("--mock", action="store_true", help="mock server")
    parser.add_argument("--no-callback", action="store_true", help="不使用HTTP回调")

    return parser.parse_args()


def validate_args(args):
    # 验证本地文件格式
    if args.local_file:
        valid_extensions = [".bin", ".pth", ".pt"]
        if not any(args.local_file.endswith(ext) for ext in valid_extensions):
            print(f"错误：本地文件必须是以下格式之一：{', '.join(valid_extensions)}")
            sys.exit(1)


async def main():
    def print_command_args():
        print("Command line arguments:")
        print(" ".join(sys.argv))
        print("\n")

    # Call at the beginning of main to display arguments
    print_command_args()
    args = parse_args()
    validate_args(args)

    # TODO: 在这里实现具体的防御逻辑
    print(f"项目UUID: {args.uuid}")
    print(f"模型类型: {args.model_type}")
    if args.url:
        print(f"模型URL: {args.url}")
    else:
        print(f"本地模型文件: {args.local_file}")
    print(f"防御方法: {', '.join(args.defense_methods)}")

    # 持久化配置
    print(f"ProtoShield路径: {args.proto_shield_path}")
    print(f"检测模式: {args.detect_mode}")
    print(f"中毒率: {args.posion_rate}")

    # 检查是否使用mock
    if args.mock:
        print("使用mock软件进行检测")

    if args.no_callback:
        print("不使用HTTP回调")
        api_client = MockClient()
    else:
        api_client = APIClient(
            base_url=f"http://localhost:13000/api/v1/projects/{args.uuid}"
        )

    # 持久化传入的通用配置
    if args.detect_mode == "app":
        detect_mode = "app"
    elif args.detect_mode == "exp":
        detect_mode = "exp"
    else:
        detect_modes = ["app", "exp"]
        print(f"错误：检测模式必须是以下之一：{', '.join(detect_modes)}")
        sys.exit(1)

    if args.posion_rate:
        posion_rate = float(args.posion_rate)
    else:
        posion_rate = 0.1

    proto_shield_path = args.proto_shield_path
    InitProtoShieldPath(proto_shield_path)

    if args.mock:
        # mock检测
        options = URLOptions(
            args.uuid,
            args.model_type,
            args.defense_methods,
            args.url,
            proto_shield_path,
            detect_mode,
            posion_rate,
        )
        detect = MockDetect()
    elif args.url:
        # 使用url的模型
        options = URLOptions(
            args.uuid,
            args.model_type,
            args.defense_methods,
            args.url,
            proto_shield_path,
            detect_mode,
            posion_rate,
        )
        detect = URLDetect()
    else:
        # 使用本地模型
        options = FileOptions(
            args.uuid,
            args.model_type,
            args.defense_methods,
            args.local_file,
            proto_shield_path,
            detect_mode,
            posion_rate,
        )
        detect = FileDetect()

    await detect.run(options, api_client)
    # print(result)


if __name__ == "__main__":
    asyncio.run(main())

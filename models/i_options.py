from abc import ABC
from typing import List, Optional


class IOptions(ABC):
    """检测选项接口基类"""

    def __init__(
        self,
        uuid: str,
        model_type: str,
        defense_methods: List[str],
        proto_shield_path: str,
        detect_mode: str,
        posion_rate: float,
    ):
        self.uuid = uuid
        self.model_type = model_type
        self.defense_methods = defense_methods
        self.proto_shield_path = proto_shield_path
        self.detect_mode = detect_mode
        self.posion_rate = posion_rate

    def validate(self) -> bool:
        """验证选项是否有效"""
        raise NotImplementedError

    def to_dict(self) -> dict:
        """转换为字典格式"""
        raise NotImplementedError

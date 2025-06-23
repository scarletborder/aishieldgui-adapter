from typing import List
from .i_options import IOptions


class FileOptions(IOptions):
    """文件检测选项"""

    def __init__(
        self,
        uuid: str,
        model_type: str,
        defense_methods: List[str],
        local_file: str,
        proto_shield_path: str,
        detect_mode: str,
        posion_rate: float,
    ):
        super().__init__(
            uuid,
            model_type,
            defense_methods,
            proto_shield_path,
            detect_mode,
            posion_rate,
        )
        self.local_file = local_file

    def validate(self) -> bool:
        """验证文件检测选项"""
        import os

        # 验证基本参数
        if not self.uuid or not self.model_type or not self.defense_methods:
            return False

        # 验证模型类型
        valid_model_types = ["QWEN", "LLAMA", "BERT"]
        if self.model_type not in valid_model_types:
            return False

        # 验证防御方法
        valid_defense_methods = [
            "MODELDEFENSETYPEONION",
            "MODELDEFENSETYPECUBE",
            "MODELDEFENSETYPESTRIP",
            "MODELDEFENSETYPEPROTO_SHIELD",
        ]
        if not all(method in valid_defense_methods for method in self.defense_methods):
            return False

        # 验证本地文件
        if not self.local_file or not os.path.exists(self.local_file):
            return False

        return True

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "uuid": self.uuid,
            "model-type": self.model_type,
            "defense-methods": self.defense_methods,
            "local-file": self.local_file,
        }

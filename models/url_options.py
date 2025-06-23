from typing import List
from .i_options import IOptions


class URLOptions(IOptions):
    """URL检测选项"""

    def __init__(
        self,
        uuid: str,
        model_type: str,
        defense_methods: List[str],
        url: str,
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
        self.url = url

    def validate(self) -> bool:
        """验证URL检测选项"""
        from urllib.parse import urlparse

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

        # 验证URL
        if not self.url:
            return False
        try:
            result = urlparse(self.url)
            if not all([result.scheme, result.netloc]):
                return False
        except:
            return False

        return True

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "uuid": self.uuid,
            "model-type": self.model_type,
            "defense-methods": self.defense_methods,
            "url": self.url,
        }

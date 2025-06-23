from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class BackdoorInjectionLayer:
    """后门注入层信息"""

    layer_name: str
    is_injected: bool
    backdoor_types: Dict[str, int] = field(default_factory=dict)


@dataclass
class RadarChartData:
    """雷达图数据"""

    mean: float
    variance: float
    outlier_ratio: float


@dataclass
class ResultItem:
    """检测结果数据模型"""

    Uuid: str
    ModelStatus: str = ""
    ConfidenceScore: float = 0.0
    TriggerTypeDistribution: Dict[str, int] = field(default_factory=dict)
    BackdoorInjectionLayers: List[BackdoorInjectionLayer] = field(default_factory=list)
    RadarChart: Dict[str, RadarChartData] = field(default_factory=dict)
    CreatedAt: datetime = field(default_factory=datetime.now)
    UpdatedAt: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，符合 Go 结构体定义"""
        return {
            "uuid": self.Uuid,
            "model_status": self.ModelStatus,
            "confidence_score": self.ConfidenceScore,
            "trigger_type_distribution": self.TriggerTypeDistribution,
            "backdoor_injection_layers": [
                {
                    "layer_name": layer.layer_name,
                    "is_injected": layer.is_injected,
                    "backdoor_types": layer.backdoor_types,
                }
                for layer in self.BackdoorInjectionLayers
            ],
            "radar_chart": {
                layer_name: {
                    "mean": data.mean,
                    "variance": data.variance,
                    "outlier_ratio": data.outlier_ratio,
                }
                for layer_name, data in self.RadarChart.items()
            },
            "created_at": self.CreatedAt.isoformat(),
            "updated_at": self.UpdatedAt.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResultItem":
        """从字典创建实例"""
        # 处理日期时间字段
        created_at = datetime.fromisoformat(
            data.get("CreatedAt", datetime.now().isoformat())
        )
        updated_at = datetime.fromisoformat(
            data.get("UpdatedAt", datetime.now().isoformat())
        )

        # 处理后门注入层
        backdoor_layers = [
            BackdoorInjectionLayer(
                layer_name=layer["layer_name"],
                is_injected=layer["is_injected"],
                backdoor_types=layer["backdoor_types"],
            )
            for layer in data.get("BackdoorInjectionLayers", [])
        ]

        # 处理雷达图数据
        radar_chart = {
            layer_name: RadarChartData(
                mean=chart_data["mean"],
                variance=chart_data["variance"],
                outlier_ratio=chart_data["outlier_ratio"],
            )
            for layer_name, chart_data in data.get("RadarChart", {}).items()
        }

        return cls(
            Uuid=data["Uuid"],
            ModelStatus=data.get("ModelStatus", ""),
            ConfidenceScore=data.get("ConfidenceScore", 0.0),
            TriggerTypeDistribution=data.get("TriggerTypeDistribution", {}),
            BackdoorInjectionLayers=backdoor_layers,
            RadarChart=radar_chart,
            CreatedAt=created_at,
            UpdatedAt=updated_at,
        )

    def update(self, data: Dict[str, Any]) -> None:
        """更新结果数据"""
        self.ModelStatus = data.get("ModelStatus", self.ModelStatus)
        self.ConfidenceScore = data.get("ConfidenceScore", self.ConfidenceScore)
        self.TriggerTypeDistribution.update(data.get("TriggerTypeDistribution", {}))

        # 更新后门注入层
        if "BackdoorInjectionLayers" in data:
            self.BackdoorInjectionLayers = [
                BackdoorInjectionLayer(
                    layer_name=layer["layer_name"],
                    is_injected=layer["is_injected"],
                    backdoor_types=layer["backdoor_types"],
                )
                for layer in data["BackdoorInjectionLayers"]
            ]

        # 更新雷达图数据
        if "RadarChart" in data:
            self.RadarChart = {
                layer_name: RadarChartData(
                    mean=chart_data["mean"],
                    variance=chart_data["variance"],
                    outlier_ratio=chart_data["outlier_ratio"],
                )
                for layer_name, chart_data in data["RadarChart"].items()
            }

        self.UpdatedAt = datetime.now()

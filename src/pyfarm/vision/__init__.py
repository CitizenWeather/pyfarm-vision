"""pyfarm-vision: Camera monitoring and growth stage identification."""

from pyfarm.vision.behavior import VisionBehavior
from pyfarm.vision.calculator import VisionCalculator
from pyfarm.vision.models import (
    DetectionClass,
    DetectionResult,
    GrowthStageEstimate,
    VisionFrame,
)

__version__ = "0.1.0"

__all__ = [
    "VisionFrame",
    "DetectionClass",
    "DetectionResult",
    "GrowthStageEstimate",
    "VisionCalculator",
    "VisionBehavior",
]

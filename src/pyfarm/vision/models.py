"""Data models for vision."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class DetectionClass(str, Enum):
    HEALTHY = "healthy"
    DEFICIENT = "deficient"
    CONTAMINATED = "contaminated"
    PEST = "pest"
    DISEASED = "diseased"
    UNKNOWN = "unknown"


@dataclass
class VisionFrame:
    timestamp: datetime = field(default_factory=datetime.utcnow)
    camera_id: str = ""
    image_path: str = ""

    def __post_init__(self):
        if not self.camera_id:
            raise ValueError("camera_id is required")


@dataclass
class DetectionResult:
    frame: VisionFrame = field(default_factory=lambda: VisionFrame(camera_id="stub"))
    detection_class: DetectionClass = DetectionClass.UNKNOWN
    confidence: float = 0.0
    bounding_boxes: list[tuple[int, int, int, int]] = field(default_factory=list)

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be 0-1")


@dataclass
class GrowthStageEstimate:
    estimated_stage: int = 0
    confidence: float = 0.0
    notes: str = ""

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be 0-1")
        if self.estimated_stage < 0:
            raise ValueError("estimated_stage must be non-negative")

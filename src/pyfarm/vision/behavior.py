"""Vision behavior — camera monitoring and detection stubs."""

from __future__ import annotations

from pyfarm.pathology.models import PathogenRisk, Pathogen, PathogenType
from pyfarm.vision.calculator import VisionCalculator
from pyfarm.vision.models import (
    DetectionClass,
    DetectionResult,
    GrowthStageEstimate,
    VisionFrame,
)


class VisionBehavior:
    """Stub vision behavior — real implementation requires an external model backend."""

    def __init__(self):
        self.calculator = VisionCalculator()

    async def analyse_frame(self, frame: VisionFrame) -> DetectionResult:
        """Analyse a single camera frame (stub — returns healthy with 0.5 confidence)."""
        return DetectionResult(
            frame=frame,
            detection_class=DetectionClass.HEALTHY,
            confidence=0.5,
        )

    async def estimate_growth_stage(
        self,
        frame: VisionFrame,
        expected_heights: list[float] | None = None,
    ) -> GrowthStageEstimate:
        """Estimate growth stage from a frame (stub)."""
        return GrowthStageEstimate(
            estimated_stage=0,
            confidence=0.5,
            notes="stub — no model backend registered",
        )

    async def check_contamination(self, frame: VisionFrame) -> list[DetectionResult]:
        """Check a frame for contamination/disease (stub returns empty list)."""
        result = await self.analyse_frame(frame)
        if result.detection_class in (
            DetectionClass.CONTAMINATED,
            DetectionClass.DISEASED,
            DetectionClass.PEST,
        ):
            return [result]
        return []

    def pathogen_risk_from_detection(
        self, result: DetectionResult
    ) -> PathogenRisk | None:
        """Map a DetectionResult to a PathogenRisk (for integration with pyfarm-pathology)."""
        class_to_type = {
            DetectionClass.DISEASED: PathogenType.FUNGAL,
            DetectionClass.CONTAMINATED: PathogenType.BACTERIAL,
            DetectionClass.PEST: PathogenType.PEST,
        }
        ptype = class_to_type.get(result.detection_class)
        if ptype is None:
            return None
        return PathogenRisk(
            pathogen=Pathogen(
                name=result.detection_class.value,
                type=ptype,
            ),
            risk_score=result.confidence,
            contributing_factors=["visual_detection"],
        )

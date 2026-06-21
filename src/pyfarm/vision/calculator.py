"""Vision calculations."""

from __future__ import annotations

from pyfarm.vision.models import DetectionClass, DetectionResult


class VisionCalculator:

    @staticmethod
    def confidence_weighted_class(results: list[DetectionResult]) -> DetectionClass:
        """Return the detection class with highest sum of confidence scores."""
        if not results:
            return DetectionClass.UNKNOWN

        scores: dict[DetectionClass, float] = {}
        for r in results:
            scores[r.detection_class] = scores.get(r.detection_class, 0.0) + r.confidence

        return max(scores, key=lambda k: scores[k])

    @staticmethod
    def growth_stage_from_height(
        height_cm: float,
        expected_heights: list[float],
    ) -> int:
        """Estimate growth stage index based on measured plant height."""
        if not expected_heights:
            return 0
        for i, h in enumerate(expected_heights):
            if height_cm <= h:
                return i
        return len(expected_heights) - 1

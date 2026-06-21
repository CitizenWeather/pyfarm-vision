"""Smoke tests for pyfarm-vision."""

import pytest

from pyfarm.vision import (
    VisionBehavior,
    VisionCalculator,
    VisionFrame,
    DetectionClass,
    DetectionResult,
    GrowthStageEstimate,
)
from pyfarm.pathology.models import PathogenRisk


def test_vision_frame_validation():
    with pytest.raises(ValueError):
        VisionFrame(camera_id="")


def test_detection_result_confidence_range():
    frame = VisionFrame(camera_id="cam-01")
    with pytest.raises(ValueError):
        DetectionResult(frame=frame, confidence=1.5)


def test_growth_stage_estimate_validation():
    with pytest.raises(ValueError):
        GrowthStageEstimate(estimated_stage=-1)
    with pytest.raises(ValueError):
        GrowthStageEstimate(confidence=2.0)


def test_confidence_weighted_class_empty():
    assert VisionCalculator.confidence_weighted_class([]) == DetectionClass.UNKNOWN


def test_confidence_weighted_class():
    frame = VisionFrame(camera_id="cam-01")
    results = [
        DetectionResult(frame=frame, detection_class=DetectionClass.HEALTHY, confidence=0.8),
        DetectionResult(frame=frame, detection_class=DetectionClass.DISEASED, confidence=0.3),
        DetectionResult(frame=frame, detection_class=DetectionClass.HEALTHY, confidence=0.6),
    ]
    cls = VisionCalculator.confidence_weighted_class(results)
    assert cls == DetectionClass.HEALTHY


def test_growth_stage_from_height():
    heights = [5.0, 15.0, 30.0, 50.0]
    assert VisionCalculator.growth_stage_from_height(3.0, heights) == 0
    assert VisionCalculator.growth_stage_from_height(20.0, heights) == 2
    assert VisionCalculator.growth_stage_from_height(100.0, heights) == 3


@pytest.mark.asyncio
async def test_analyse_frame():
    behavior = VisionBehavior()
    frame = VisionFrame(camera_id="cam-01", image_path="/tmp/frame.jpg")
    result = await behavior.analyse_frame(frame)
    assert isinstance(result, DetectionResult)
    assert result.detection_class == DetectionClass.HEALTHY


@pytest.mark.asyncio
async def test_estimate_growth_stage():
    behavior = VisionBehavior()
    frame = VisionFrame(camera_id="cam-01")
    estimate = await behavior.estimate_growth_stage(frame)
    assert isinstance(estimate, GrowthStageEstimate)


@pytest.mark.asyncio
async def test_check_contamination_healthy():
    behavior = VisionBehavior()
    frame = VisionFrame(camera_id="cam-01")
    results = await behavior.check_contamination(frame)
    assert results == []


def test_pathogen_risk_from_detection_healthy():
    behavior = VisionBehavior()
    frame = VisionFrame(camera_id="cam-01")
    result = DetectionResult(frame=frame, detection_class=DetectionClass.HEALTHY, confidence=0.9)
    risk = behavior.pathogen_risk_from_detection(result)
    assert risk is None


def test_pathogen_risk_from_detection_diseased():
    behavior = VisionBehavior()
    frame = VisionFrame(camera_id="cam-01")
    result = DetectionResult(frame=frame, detection_class=DetectionClass.DISEASED, confidence=0.7)
    risk = behavior.pathogen_risk_from_detection(result)
    assert isinstance(risk, PathogenRisk)
    assert risk.risk_score == 0.7

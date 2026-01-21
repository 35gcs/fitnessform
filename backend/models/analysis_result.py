from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class FormIssue(BaseModel):
    issue: str
    severity: Severity
    description: str
    timestamp: Optional[float] = None
    frames: Optional[List[int]] = None


class CorrectiveExercise(BaseModel):
    name: str
    description: str
    sets: str
    reps: str
    focus: str


class AnalysisResult(BaseModel):
    exercise: str
    overall_score: float
    issues: List[FormIssue]
    recommendations: List[str]
    corrective_exercises: List[CorrectiveExercise]
    summary: str
    frame_count: int

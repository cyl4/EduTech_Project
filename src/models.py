from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class PresentationMode(str, Enum):
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    LAYPERSON = "layperson"
    CASUAL = "casual"
    CUSTOM = "custom"

class AudioMetrics(BaseModel):
    transcription: str
    pace: float  # words per minute
    tone: float  # average pitch
    filler_words: List[str]
    filler_count: int
    intonation_variance: float
    clarity_score: float

class ContentAnalysis(BaseModel):
    clarity_score: float
    flow_score: float
    technical_accuracy: float
    explanation_quality: float
    suggested_improvements: List[str]

class PresentationScore(BaseModel):
    overall_score: float
    audio_metrics: AudioMetrics
    content_analysis: ContentAnalysis
    mode: PresentationMode
    topic: str
    timestamp: str

class Question(BaseModel):
    question: str
    category: str
    difficulty: str
    context: Optional[str] = None

class Suggestion(BaseModel):
    type: str  # metaphor, analogy, image
    suggestion: str
    context: str
    confidence: float

class PresentationSession(BaseModel):
    session_id: str
    mode: PresentationMode
    topic: str
    custom_context: Optional[str] = None
    expert_documents: Optional[List[str]] = None
    scores: List[PresentationScore] = []
    questions: List[Question] = []
    suggestions: List[Suggestion] = []


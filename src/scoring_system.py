from typing import Dict, Any
from .models import AudioMetrics, ContentAnalysis, PresentationScore, PresentationMode
import datetime

class ScoringSystem:
    def __init__(self):
        self.weights = {
            'audio': 0.3,
            'content': 0.7
        }
        
        self.audio_weights = {
            'pace': 0.2,
            'tone': 0.1,
            'filler_words': 0.3,
            'intonation_variance': 0.2,
            'clarity_score': 0.2
        }
        
        self.content_weights = {
            'clarity_score': 0.3,
            'flow_score': 0.25,
            'technical_accuracy': 0.25,
            'explanation_quality': 0.2
        }
    
    def calculate_overall_score(self, audio_metrics: AudioMetrics, content_analysis: ContentAnalysis, 
                              mode: PresentationMode, topic: str) -> PresentationScore:
        """Calculate overall presentation score"""
        
        # Calculate audio score
        audio_score = self._calculate_audio_score(audio_metrics)
        
        # Calculate content score
        content_score = self._calculate_content_score(content_analysis)
        
        # Calculate overall score
        overall_score = (
            audio_score * self.weights['audio'] + 
            content_score * self.weights['content']
        )
        
        # Adjust for mode
        overall_score = self._adjust_for_mode(overall_score, mode)
        
        return PresentationScore(
            overall_score=overall_score,
            audio_metrics=audio_metrics,
            content_analysis=content_analysis,
            mode=mode,
            topic=topic,
            timestamp=datetime.datetime.now().isoformat()
        )
    
    def _calculate_audio_score(self, audio_metrics: AudioMetrics) -> float:
        """Calculate audio component score"""
        
        # Pace score (optimal range: 120-180 WPM)
        if 120 <= audio_metrics.pace <= 180:
            pace_score = 1.0
        elif 100 <= audio_metrics.pace < 120 or 180 < audio_metrics.pace <= 200:
            pace_score = 0.7
        else:
            pace_score = 0.4
        
        # Filler words score (lower is better)
        filler_score = max(0, 1.0 - (audio_metrics.filler_count * 0.1))
        
        # Intonation variance score (moderate variance is good)
        if 0.5 <= audio_metrics.intonation_variance <= 2.0:
            intonation_score = 1.0
        elif 0.2 <= audio_metrics.intonation_variance < 0.5 or 2.0 < audio_metrics.intonation_variance <= 3.0:
            intonation_score = 0.7
        else:
            intonation_score = 0.4
        
        # Clarity score (direct from audio analysis)
        clarity_score = audio_metrics.clarity_score
        
        # Tone score (moderate pitch is generally better)
        if 100 <= audio_metrics.tone <= 300:
            tone_score = 1.0
        elif 80 <= audio_metrics.tone < 100 or 300 < audio_metrics.tone <= 400:
            tone_score = 0.7
        else:
            tone_score = 0.4
        
        return (
            pace_score * self.audio_weights['pace'] +
            tone_score * self.audio_weights['tone'] +
            filler_score * self.audio_weights['filler_words'] +
            intonation_score * self.audio_weights['intonation_variance'] +
            clarity_score * self.audio_weights['clarity_score']
        )
    
    def _calculate_content_score(self, content_analysis: ContentAnalysis) -> float:
        """Calculate content component score"""
        
        return (
            content_analysis.clarity_score * self.content_weights['clarity_score'] +
            content_analysis.flow_score * self.content_weights['flow_score'] +
            content_analysis.technical_accuracy * self.content_weights['technical_accuracy'] +
            content_analysis.explanation_quality * self.content_weights['explanation_quality']
        )
    
    def _adjust_for_mode(self, score: float, mode: PresentationMode) -> float:
        """Adjust score based on presentation mode"""
        
        mode_adjustments = {
            PresentationMode.PROFESSIONAL: 1.0,  # No adjustment
            PresentationMode.TECHNICAL: 0.95,    # Slightly more lenient
            PresentationMode.LAYPERSON: 1.05,    # Slightly more strict
            PresentationMode.CASUAL: 0.9,        # More lenient
            PresentationMode.CUSTOM: 1.0         # No adjustment
        }
        
        return score * mode_adjustments.get(mode, 1.0)
    
    def get_score_breakdown(self, score: PresentationScore) -> Dict[str, Any]:
        """Get detailed score breakdown for feedback"""
        
        return {
            'overall_score': score.overall_score,
            'audio_score': self._calculate_audio_score(score.audio_metrics),
            'content_score': self._calculate_content_score(score.content_analysis),
            'breakdown': {
                'pace': {
                    'score': self._get_pace_score(score.audio_metrics.pace),
                    'value': score.audio_metrics.pace,
                    'feedback': self._get_pace_feedback(score.audio_metrics.pace)
                },
                'filler_words': {
                    'score': max(0, 1.0 - (score.audio_metrics.filler_count * 0.1)),
                    'value': score.audio_metrics.filler_count,
                    'feedback': self._get_filler_feedback(score.audio_metrics.filler_count)
                },
                'clarity': {
                    'score': score.content_analysis.clarity_score,
                    'feedback': self._get_clarity_feedback(score.content_analysis.clarity_score)
                },
                'flow': {
                    'score': score.content_analysis.flow_score,
                    'feedback': self._get_flow_feedback(score.content_analysis.flow_score)
                }
            }
        }
    
    def _get_pace_score(self, pace: float) -> float:
        """Get pace score"""
        if 120 <= pace <= 180:
            return 1.0
        elif 100 <= pace < 120 or 180 < pace <= 200:
            return 0.7
        else:
            return 0.4
    
    def _get_pace_feedback(self, pace: float) -> str:
        """Get pace feedback"""
        if pace < 100:
            return "Speaking too slowly. Try to increase your pace."
        elif pace > 200:
            return "Speaking too quickly. Slow down for better comprehension."
        elif 120 <= pace <= 180:
            return "Excellent speaking pace!"
        else:
            return "Good pace, but could be slightly adjusted."
    
    def _get_filler_feedback(self, filler_count: int) -> str:
        """Get filler words feedback"""
        if filler_count == 0:
            return "No filler words detected - excellent!"
        elif filler_count <= 3:
            return "Minimal filler words - good job!"
        elif filler_count <= 6:
            return "Some filler words detected. Practice pausing instead."
        else:
            return "Too many filler words. Focus on clear pauses."
    
    def _get_clarity_feedback(self, clarity_score: float) -> str:
        """Get clarity feedback"""
        if clarity_score >= 0.8:
            return "Excellent clarity and explanation quality!"
        elif clarity_score >= 0.6:
            return "Good clarity, but could be improved."
        else:
            return "Clarity needs improvement. Consider simplifying explanations."
    
    def _get_flow_feedback(self, flow_score: float) -> str:
        """Get flow feedback"""
        if flow_score >= 0.8:
            return "Excellent flow and organization!"
        elif flow_score >= 0.6:
            return "Good flow, but transitions could be smoother."
        else:
            return "Flow needs improvement. Work on better transitions between ideas."

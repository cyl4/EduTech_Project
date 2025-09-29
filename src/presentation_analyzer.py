import asyncio
import tempfile
import os
from typing import List, Optional, Dict, Any
from .models import PresentationSession, PresentationMode, PresentationScore, Question, Suggestion
from .audio_analyzer import AudioAnalyzer
from .content_analyzer import ContentAnalyzer
from .question_generator import QuestionGenerator
from .suggestion_engine import SuggestionEngine
from .scoring_system import ScoringSystem

class PresentationAnalyzer:
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
        self.content_analyzer = ContentAnalyzer()
        self.question_generator = QuestionGenerator()
        self.suggestion_engine = SuggestionEngine()
        self.scoring_system = ScoringSystem()
        self.sessions: Dict[str, PresentationSession] = {}
    
    def create_session(self, session_id: str, mode: PresentationMode, topic: str, 
                      custom_context: str = None, expert_documents: List[str] = None) -> PresentationSession:
        """Create a new presentation session"""
        
        session = PresentationSession(
            session_id=session_id,
            mode=mode,
            topic=topic,
            custom_context=custom_context,
            expert_documents=expert_documents
        )
        
        self.sessions[session_id] = session
        return session
    
    async def analyze_presentation_chunk(self, session_id: str, audio_data: bytes, 
                                       transcript: str) -> PresentationScore:
        """Analyze a chunk of presentation audio and text"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Analyze audio
        audio_metrics = self.audio_analyzer.analyze_audio(audio_data)
        
        # Analyze content
        content_analysis = await self.content_analyzer.analyze_content(
            transcript, session.topic, session.mode, session.custom_context
        )
        
        # Calculate overall score
        score = self.scoring_system.calculate_overall_score(
            audio_metrics, content_analysis, session.mode, session.topic
        )
        
        # Add to session
        session.scores.append(score)
        
        return score
    
    async def generate_questions_for_session(self, session_id: str, transcript: str) -> List[Question]:
        """Generate questions for a session"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        questions = await self.question_generator.generate_questions(
            transcript, session.topic, session.mode, session.expert_documents
        )
        
        session.questions.extend(questions)
        return questions
    
    async def generate_suggestions_for_session(self, session_id: str, transcript: str) -> List[Suggestion]:
        """Generate suggestions for improving unclear explanations"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Detect unclear explanations
        unclear_sentences = self.content_analyzer.detect_unclear_explanations(transcript)
        
        if not unclear_sentences:
            return []
        
        # Generate suggestions
        suggestions = await self.suggestion_engine.generate_suggestions(
            transcript, session.topic, session.mode, unclear_sentences
        )
        
        session.suggestions.extend(suggestions)
        return suggestions
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        if not session.scores:
            return {"error": "No scores available for this session"}
        
        # Calculate average scores
        avg_overall = sum(score.overall_score for score in session.scores) / len(session.scores)
        avg_audio = sum(score.audio_metrics.clarity_score for score in session.scores) / len(session.scores)
        avg_content = sum(score.content_analysis.clarity_score for score in session.scores) / len(session.scores)
        
        # Get latest score breakdown
        latest_score = session.scores[-1]
        score_breakdown = self.scoring_system.get_score_breakdown(latest_score)
        
        return {
            'session_id': session_id,
            'topic': session.topic,
            'mode': session.mode.value,
            'total_chunks': len(session.scores),
            'average_scores': {
                'overall': avg_overall,
                'audio': avg_audio,
                'content': avg_content
            },
            'latest_score_breakdown': score_breakdown,
            'total_questions': len(session.questions),
            'total_suggestions': len(session.suggestions),
            'suggestions': [s.dict() for s in session.suggestions[-5:]],  # Last 5 suggestions
            'questions': [q.dict() for q in session.questions[-5:]]  # Last 5 questions
        }
    
    def get_session(self, session_id: str) -> Optional[PresentationSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

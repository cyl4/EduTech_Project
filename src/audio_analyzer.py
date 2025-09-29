import librosa
import numpy as np
from typing import List, Tuple
from models import AudioMetrics
from speech_to_text import SpeechToText
from senselab import SpeechAnalyzer

class AudioAnalyzer:
    def __init__(self, stt_model_path: str = "base", device: str = "cpu"):
        self.speech_analyzer = SpeechAnalyzer()
        self.speech_to_text = SpeechToText(model_path=stt_model_path, device=device)

    def analyze_audio(self, audio_path: str, sample_rate: int = 16000) -> AudioMetrics:
        """Analyze audio for presentation metrics and transcription using SenseLab."""
        try:
            # Step 1: Analyze audio using SenseLab
            analysis_result = self.speech_analyzer.analyze(audio_path)

            # Extract metrics from SenseLab's result
            transcription = analysis_result.transcription
            language = analysis_result.language
            pace = analysis_result.pace
            tone = analysis_result.tone
            filler_words = analysis_result.filler_words
            filler_count = len(filler_words)
            intonation_variance = analysis_result.intonation_variance
            clarity_score = analysis_result.clarity_score

            return AudioMetrics(
                pace=pace,
                tone=tone,
                filler_words=filler_words,
                filler_count=filler_count,
                intonation_variance=intonation_variance,
                clarity_score=clarity_score,
                transcription=transcription,
                language=language
            )
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return AudioMetrics(
                pace=0.0,
                tone=0.0,
                filler_words=[],
                filler_count=0,
                intonation_variance=0.0,
                clarity_score=0.0,
                transcription="",
                language=""
            )

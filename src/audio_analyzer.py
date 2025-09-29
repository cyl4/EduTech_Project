import librosa
import numpy as np
from typing import List, Tuple
import re
from .models import AudioMetrics

class AudioAnalyzer:
    def __init__(self):
        self.filler_words = [
            'um', 'uh', 'like', 'you know', 'so', 'well', 'actually',
            'basically', 'literally', 'right', 'okay', 'alright'
        ]
    
    def analyze_audio(self, audio_data: bytes, sample_rate: int = 16000) -> AudioMetrics:
        """Analyze audio for presentation metrics"""
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Extract features
            pace = self._calculate_pace(audio_array, sample_rate)
            tone = self._calculate_tone(audio_array, sample_rate)
            filler_words, filler_count = self._detect_filler_words(audio_array, sample_rate)
            intonation_variance = self._calculate_intonation_variance(audio_array, sample_rate)
            clarity_score = self._calculate_clarity_score(audio_array, sample_rate)
            
            return AudioMetrics(
                pace=pace,
                tone=tone,
                filler_words=filler_words,
                filler_count=filler_count,
                intonation_variance=intonation_variance,
                clarity_score=clarity_score
            )
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return AudioMetrics(
                pace=0.0,
                tone=0.0,
                filler_words=[],
                filler_count=0,
                intonation_variance=0.0,
                clarity_score=0.0
            )
    
    def _calculate_pace(self, audio: np.ndarray, sample_rate: int) -> float:
        """Calculate speaking pace in words per minute"""
        # Simple energy-based speech detection
        frame_length = int(0.025 * sample_rate)  # 25ms frames
        hop_length = int(0.010 * sample_rate)    # 10ms hop
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Detect speech segments
        speech_threshold = np.mean(rms) * 0.3
        speech_frames = rms > speech_threshold
        
        # Estimate speaking time
        speaking_time = np.sum(speech_frames) * hop_length / sample_rate
        
        # Rough estimate: average speaking rate is 150-160 WPM
        # This is a simplified calculation
        if speaking_time > 0:
            estimated_words = len(audio) / (sample_rate * 60) * 150  # rough estimate
            return estimated_words / (speaking_time / 60) if speaking_time > 0 else 0
        return 0
    
    def _calculate_tone(self, audio: np.ndarray, sample_rate: int) -> float:
        """Calculate average pitch/tone"""
        try:
            # Extract pitch using librosa
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sample_rate, threshold=0.1)
            
            # Get non-zero pitches
            non_zero_pitches = pitches[pitches > 0]
            
            if len(non_zero_pitches) > 0:
                return float(np.mean(non_zero_pitches))
            return 0.0
        except:
            return 0.0
    
    def _detect_filler_words(self, audio: np.ndarray, sample_rate: int) -> Tuple[List[str], int]:
        """Detect filler words in audio"""
        # This is a simplified implementation
        # In a real system, you'd use speech recognition first
        # For now, return empty list
        return [], 0
    
    def _calculate_intonation_variance(self, audio: np.ndarray, sample_rate: int) -> float:
        """Calculate variance in intonation"""
        try:
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sample_rate, threshold=0.1)
            non_zero_pitches = pitches[pitches > 0]
            
            if len(non_zero_pitches) > 1:
                return float(np.std(non_zero_pitches))
            return 0.0
        except:
            return 0.0
    
    def _calculate_clarity_score(self, audio: np.ndarray, sample_rate: int) -> float:
        """Calculate clarity score based on audio quality"""
        try:
            # Calculate signal-to-noise ratio
            rms = librosa.feature.rms(y=audio)[0]
            noise_floor = np.percentile(rms, 10)
            signal_level = np.percentile(rms, 90)
            
            if noise_floor > 0:
                snr = 20 * np.log10(signal_level / noise_floor)
                # Normalize to 0-1 scale
                return min(1.0, max(0.0, (snr + 10) / 30))
            return 0.5
        except:
            return 0.5

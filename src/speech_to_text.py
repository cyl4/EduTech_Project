from faster_whisper import WhisperModel
import wave
import numpy as np
from typing import Dict, Generator

class SpeechToText:
    def __init__(self, model_path: str = "small", device: str = "cpu", local_files_only: bool = False):
        """Initialize the Whisper model."""
        self.model = WhisperModel(model_path, device=device, compute_type="int8", local_files_only=local_files_only)

    def transcribe(self, audio_path: str) -> Dict[str, str]:
        """Transcribe audio to text.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            Dict[str, str]: A dictionary containing the transcription and language.
        """
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        transcription = "".join([segment.text for segment in segments])
        return {
            "transcription": transcription,
            "language": info.language
        }

    def transcribe_stream(self, audio_stream: Generator[bytes, None, None]) -> Generator[str, None, None]:
        """Transcribe audio from a stream in real-time.

        Args:
            audio_stream (Generator[bytes, None, None]): A generator yielding chunks of audio data.

        Yields:
            str: Transcribed text for each chunk.
        """
        buffer = b""
        for chunk in audio_stream:
            buffer += chunk
            if len(buffer) > 16000 * 2 * 5:  # Process every 5 seconds of audio (assuming 16kHz, 16-bit audio)
                audio_array = np.frombuffer(buffer, dtype=np.int16)
                segments, _ = self.model.transcribe(audio_array, beam_size=5)
                for segment in segments:
                    yield segment.text
                buffer = b""  # Clear the buffer after processing

        # Process any remaining audio in the buffer
        if buffer:
            audio_array = np.frombuffer(buffer, dtype=np.int16)
            segments, _ = self.model.transcribe(audio_array, beam_size=5)
            for segment in segments:
                yield segment.text

# Example usage
if __name__ == "__main__":
    stt = SpeechToText(local_files_only=False)
    result = stt.transcribe("briskaudioclip2.wav")
    print("Transcription:", result["transcription"])
    print("Language:", result["language"])
from audio_analyzer import AudioAnalyzer
from models import AudioMetrics

def test_audio_analyzer():
    # Path to your audio file
    audio_path = "briskaudioclip2.wav"
    
    # Initialize the AudioAnalyzer
    analyzer = AudioAnalyzer(stt_model_path="base", device="cpu")
    
    # Analyze the audio file
    result: AudioMetrics = analyzer.analyze_audio(audio_path)
    # Print the results
    print("Transcription:", result.transcription)
    #print("Language:", result.language)
    print("Pace:", result.pace)
    print("Tone:", result.tone)
    print("Filler Words:", result.filler_words)
    print("Filler Count:", result.filler_count)
    print("Intonation Variance:", result.intonation_variance)
    print("Clarity Score:", result.clarity_score)

# Run the test
if __name__ == "__main__":
    test_audio_analyzer()
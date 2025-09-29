from speech_to_text import SpeechToText
from content_analyzer import ContentAnalyzer
from scoring_system import ScoringSystem
from models import PresentationMode, ContentAnalysis

class FeedbackPipeline:
    def __init__(self, stt_model_path="base", device="cpu"):
        """Initialize the pipeline components."""
        self.speech_to_text = SpeechToText(model_path=stt_model_path, device=device)
        self.content_analyzer = ContentAnalyzer()
        self.scoring_system = ScoringSystem()

    async def process_audio(self, audio_path: str, topic: str, mode: PresentationMode):
        """Process the audio file and provide feedback.

        Args:
            audio_path (str): Path to the audio file.
            topic (str): Topic of the presentation.
            mode (PresentationMode): Presentation mode (e.g., PROFESSIONAL, TECHNICAL).

        Returns:
            dict: Feedback report including transcription, analysis, and scores.
        """
        # Step 1: Transcribe audio
        transcription_result = self.speech_to_text.transcribe(audio_path)
        transcription = transcription_result["transcription"]
        language = transcription_result["language"]

        # Step 2: Analyze transcription
        analysis: ContentAnalysis = await self.content_analyzer.analyze_content(
            transcript=transcription,
            topic=topic,
            mode=mode
        )

        # Step 3: Score the analysis
        scores = self.scoring_system.calculate_scores(analysis)

        # Step 4: Compile feedback
        feedback = {
            "transcription": transcription,
            "language": language,
            "analysis": {
                "clarity_score": analysis.clarity_score,
                "flow_score": analysis.flow_score,
                "technical_accuracy": analysis.technical_accuracy,
                "explanation_quality": analysis.explanation_quality,
                "suggestions": analysis.suggested_improvements
            },
            "scores": scores
        }

        return feedback

# Example usage
if __name__ == "__main__":
    import asyncio
    from models import PresentationMode

    pipeline = FeedbackPipeline()
    feedback = asyncio.run(pipeline.process_audio(
        audio_path="path_to_audio_file.wav",
        topic="Artificial Intelligence",
        mode=PresentationMode.TECHNICAL
    ))

    print("Feedback Report:", feedback)
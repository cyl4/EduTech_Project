import os
from openai import OpenAI
from huggingface_hub import InferenceClient
import re
from typing import List, Dict, Any
from .models import ContentAnalysis, PresentationMode

class ContentAnalyzer:
    def __init__(self, openai_client):
        self.client = openai_client
        self.use_hf = os.getenv('USE_HF', 'false').lower() == 'true'
        self.hf_model = os.getenv('HF_CHAT_MODEL', 'meta-llama/Meta-Llama-3-8B-Instruct')
        self.hf_client = InferenceClient(model=self.hf_model) if self.use_hf else None
    
    async def analyze_content(self, transcript: str, topic: str, mode: PresentationMode, custom_context: str = None) -> ContentAnalysis:
        """Analyze presentation content for clarity and flow"""
        
        # Create context based on mode
        context_prompt = self._get_context_prompt(mode, custom_context)
        
        analysis_prompt = f"""
        Analyze this presentation transcript for clarity, flow, and explanation quality.
        
        Topic: {topic}
        Mode: {mode.value}
        {context_prompt}
        
        Transcript: {transcript}
        
        Please provide:
        1. Clarity score (0-1): How clear and understandable is the explanation?
        2. Flow score (0-1): How well do the ideas flow together?
        3. Technical accuracy (0-1): How accurate is the technical content?
        4. Explanation quality (0-1): How well are complex concepts explained?
        5. Specific suggestions for improvement
        
        Format your response as JSON:
        {{
            "clarity_score": 0.8,
            "flow_score": 0.7,
            "technical_accuracy": 0.9,
            "explanation_quality": 0.6,
            "suggestions": [
                "Consider using more concrete examples",
                "The transition between topics could be smoother"
            ]
        }}
        """
        
        try:
            import anyio, json
            if self.use_hf:
                def _run_hf():
                    # text-generation style completion; many providers support simple prompts
                    return self.hf_client.text_generation(analysis_prompt, max_new_tokens=500, temperature=0.3)
                raw = await anyio.to_thread.run_sync(_run_hf)
                content = raw
            else:
                def _run_oa():
                    return self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": analysis_prompt}],
                        temperature=0.3
                    )
                response = await anyio.to_thread.run_sync(_run_oa)
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
            return ContentAnalysis(
                clarity_score=result.get("clarity_score", 0.5),
                flow_score=result.get("flow_score", 0.5),
                technical_accuracy=result.get("technical_accuracy", 0.5),
                explanation_quality=result.get("explanation_quality", 0.5),
                suggested_improvements=result.get("suggestions", [])
            )
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return ContentAnalysis(
                clarity_score=0.5,
                flow_score=0.5,
                technical_accuracy=0.5,
                explanation_quality=0.5,
                suggested_improvements=["Analysis unavailable"]
            )
    
    def _get_context_prompt(self, mode: PresentationMode, custom_context: str = None) -> str:
        """Get context prompt based on presentation mode"""
        if mode == PresentationMode.PROFESSIONAL:
            return "This is a professional presentation. Focus on business communication standards."
        elif mode == PresentationMode.TECHNICAL:
            return "This is a technical presentation. Focus on technical accuracy and depth."
        elif mode == PresentationMode.LAYPERSON:
            return "This is for a general audience. Focus on accessibility and simplicity."
        elif mode == PresentationMode.CASUAL:
            return "This is a casual presentation. Focus on conversational flow and engagement."
        elif mode == PresentationMode.CUSTOM and custom_context:
            return f"Custom context: {custom_context}"
        else:
            return "This is a general presentation. Focus on overall communication effectiveness."
    
    def detect_unclear_explanations(self, transcript: str) -> List[str]:
        """Detect parts of the transcript that may need better explanation"""
        unclear_indicators = [
            "it's complicated",
            "hard to explain",
            "difficult to understand",
            "not sure how to put this",
            "kind of like",
            "sort of",
            "basically",
            "you know what I mean"
        ]
        
        unclear_sentences = []
        sentences = re.split(r'[.!?]+', transcript)
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(indicator in sentence_lower for indicator in unclear_indicators):
                unclear_sentences.append(sentence.strip())
        
        return unclear_sentences

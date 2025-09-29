import openai
from typing import List, Dict, Any
from .models import Suggestion, PresentationMode

class SuggestionEngine:
    def __init__(self, openai_client):
        self.client = openai_client
    
    async def generate_suggestions(self, transcript: str, topic: str, mode: PresentationMode, 
                                 unclear_sentences: List[str]) -> List[Suggestion]:
        """Generate suggestions for improving unclear explanations"""
        
        suggestions = []
        
        for sentence in unclear_sentences:
            # Generate metaphor suggestions
            metaphor_suggestions = await self._generate_metaphors(sentence, topic, mode)
            suggestions.extend(metaphor_suggestions)
            
            # Generate analogy suggestions
            analogy_suggestions = await self._generate_analogies(sentence, topic, mode)
            suggestions.extend(analogy_suggestions)
            
            # Generate image suggestions
            image_suggestions = await self._generate_image_suggestions(sentence, topic, mode)
            suggestions.extend(image_suggestions)
        
        return suggestions
    
    async def _generate_metaphors(self, sentence: str, topic: str, mode: PresentationMode) -> List[Suggestion]:
        """Generate metaphor suggestions for unclear explanations"""
        
        prompt = f"""
        The speaker said: "{sentence}"
        
        Topic: {topic}
        Mode: {mode.value}
        
        Suggest 2-3 creative metaphors that could help explain this concept more clearly.
        Consider the audience level and context.
        
        Format as JSON:
        {{
            "metaphors": [
                {{
                    "metaphor": "It's like...",
                    "explanation": "Why this metaphor works",
                    "confidence": 0.8
                }}
            ]
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            suggestions = []
            for m in result.get("metaphors", []):
                suggestions.append(Suggestion(
                    type="metaphor",
                    suggestion=m["metaphor"],
                    context=sentence,
                    confidence=m["confidence"]
                ))
            
            return suggestions
        except Exception as e:
            print(f"Error generating metaphors: {e}")
            return []
    
    async def _generate_analogies(self, sentence: str, topic: str, mode: PresentationMode) -> List[Suggestion]:
        """Generate analogy suggestions for unclear explanations"""
        
        prompt = f"""
        The speaker said: "{sentence}"
        
        Topic: {topic}
        Mode: {mode.value}
        
        Suggest 2-3 analogies that could help explain this concept more clearly.
        Use familiar, everyday examples that the audience can relate to.
        
        Format as JSON:
        {{
            "analogies": [
                {{
                    "analogy": "It's similar to how...",
                    "explanation": "Why this analogy works",
                    "confidence": 0.7
                }}
            ]
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            suggestions = []
            for a in result.get("analogies", []):
                suggestions.append(Suggestion(
                    type="analogy",
                    suggestion=a["analogy"],
                    context=sentence,
                    confidence=a["confidence"]
                ))
            
            return suggestions
        except Exception as e:
            print(f"Error generating analogies: {e}")
            return []
    
    async def _generate_image_suggestions(self, sentence: str, topic: str, mode: PresentationMode) -> List[Suggestion]:
        """Generate image suggestions for unclear explanations"""
        
        prompt = f"""
        The speaker said: "{sentence}"
        
        Topic: {topic}
        Mode: {mode.value}
        
        Suggest 2-3 types of images, diagrams, or visual aids that could help explain this concept.
        Be specific about what the image should show.
        
        Format as JSON:
        {{
            "images": [
                {{
                    "description": "A flowchart showing...",
                    "explanation": "Why this visual would help",
                    "confidence": 0.9
                }}
            ]
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            suggestions = []
            for img in result.get("images", []):
                suggestions.append(Suggestion(
                    type="image",
                    suggestion=img["description"],
                    context=sentence,
                    confidence=img["confidence"]
                ))
            
            return suggestions
        except Exception as e:
            print(f"Error generating image suggestions: {e}")
            return []

import os
from huggingface_hub import InferenceClient
from typing import List, Dict, Any
from .models import Suggestion, PresentationMode

class SuggestionEngine:
    def __init__(self):
        self.use_hf = os.getenv('USE_HF', 'false').lower() == 'true'
        self.hf_model = os.getenv('HF_CHAT_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')
        self.hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACEHUB_API_TOKEN')
        self.hf_task = os.getenv('HF_TASK', 'conversational')
        self.hf_client = InferenceClient(model=self.hf_model, token=self.hf_token) if self.use_hf else None

    
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
            import anyio, json
            if self.use_hf:
                if self.hf_task == 'conversational':
                    def _run_hf_chat():
                        return self.hf_client.chat.completions.create(
                            model=self.hf_model,
                            messages=[{"role":"user","content": prompt}],
                            temperature=0.8,
                            max_tokens=700
                        )
                    resp = await anyio.to_thread.run_sync(_run_hf_chat)
                    content = resp.choices[0].message.content
                else:
                    def _run_hf():
                        return self.hf_client.text_generation(prompt, max_new_tokens=500, temperature=0.8)
                    content = await anyio.to_thread.run_sync(_run_hf)
            else:
                def _run_oa():
                    return self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.8
                    )
                response = await anyio.to_thread.run_sync(_run_oa)
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
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
            import anyio, json
            if self.use_hf:
                if self.hf_task == 'conversational':
                    def _run_hf_chat():
                        return self.hf_client.chat.completions.create(
                            model=self.hf_model,
                            messages=[{"role":"user","content": prompt}],
                            temperature=0.8,
                            max_tokens=700
                        )
                    resp = await anyio.to_thread.run_sync(_run_hf_chat)
                    content = resp.choices[0].message.content
                else:
                    def _run_hf():
                        return self.hf_client.text_generation(prompt, max_new_tokens=500, temperature=0.8)
                    content = await anyio.to_thread.run_sync(_run_hf)
            elif self.use_grok:
                def _run_grok():
                    return self.grok_client.chat.completions.create(
                        model=self.grok_model,
                        messages=[{"role":"user","content": prompt}],
                        temperature=0.8
                    )
                resp = await anyio.to_thread.run_sync(_run_grok)
                content = resp.choices[0].message.content
            else:
                def _run_oa():
                    return self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.8
                    )
                response = await anyio.to_thread.run_sync(_run_oa)
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
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
            import anyio, json
            if self.use_hf:
                if self.hf_task == 'conversational':
                    def _run_hf_chat():
                        return self.hf_client.chat.completions.create(
                            model=self.hf_model,
                            messages=[{"role":"user","content": prompt}],
                            temperature=0.7,
                            max_tokens=700
                        )
                    resp = await anyio.to_thread.run_sync(_run_hf_chat)
                    content = resp.choices[0].message.content
                else:
                    def _run_hf():
                        return self.hf_client.text_generation(prompt, max_new_tokens=500, temperature=0.7)
                    content = await anyio.to_thread.run_sync(_run_hf)
            elif self.use_grok:
                def _run_grok():
                    return self.grok_client.chat.completions.create(
                        model=self.grok_model,
                        messages=[{"role":"user","content": prompt}],
                        temperature=0.7
                    )
                resp = await anyio.to_thread.run_sync(_run_grok)
                content = resp.choices[0].message.content
            else:
                def _run_oa():
                    return self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                response = await anyio.to_thread.run_sync(_run_oa)
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
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

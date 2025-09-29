import os
# from openai import OpenAI
from huggingface_hub import InferenceClient
from typing import List, Dict, Any
from .models import Question, PresentationMode

class QuestionGenerator:
    def __init__(self, InferenceClient):
        self.client = InferenceClient
        self.use_hf = os.getenv('USE_HF', 'false').lower() == 'true'
        self.hf_model = os.getenv('HF_CHAT_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')
        self.hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACEHUB_API_TOKEN')
        self.hf_task = os.getenv('HF_TASK', 'conversational')
        self.hf_client = InferenceClient(model=self.hf_model, token=self.hf_token) if self.use_hf else None
    
    async def generate_questions(self, transcript: str, topic: str, mode: PresentationMode, 
                               expert_documents: List[str] = None) -> List[Question]:
        """Generate questions based on presentation content and mode"""
        
        if mode == PresentationMode.TECHNICAL and expert_documents:
            return await self._generate_expert_questions(transcript, topic, expert_documents)
        else:
            return await self._generate_standard_questions(transcript, topic, mode)
    
    async def _generate_standard_questions(self, transcript: str, topic: str, mode: PresentationMode) -> List[Question]:
        """Generate standard questions for different modes"""
        
        mode_context = {
            PresentationMode.PROFESSIONAL: "professional business context",
            PresentationMode.TECHNICAL: "technical expert context", 
            PresentationMode.LAYPERSON: "general audience context",
            PresentationMode.CASUAL: "casual conversation context"
        }
        
        prompt = f"""
        Generate 3-5 thoughtful questions about this presentation that would test the speaker's understanding.
        
        Topic: {topic}
        Context: {mode_context.get(mode, 'general context')}
        Transcript: {transcript}
        
        Create questions that:
        1. Test understanding of key concepts
        2. Explore implications or applications
        3. Challenge assumptions or ask for clarification
        4. Are appropriate for the {mode.value} mode
        
        Format as JSON:
        {{
            "questions": [
                {{
                    "question": "What would happen if...",
                    "category": "application",
                    "difficulty": "medium",
                    "context": "Testing practical understanding"
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
                            max_tokens=900
                        )
                    resp = await anyio.to_thread.run_sync(_run_hf_chat)
                    content = resp.choices[0].message.content
                else:
                    def _run_hf():
                        return self.hf_client.text_generation(prompt, max_new_tokens=600, temperature=0.7)
                    content = await anyio.to_thread.run_sync(_run_hf)
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
            
            questions = []
            for q in result.get("questions", []):
                questions.append(Question(
                    question=q["question"],
                    category=q["category"],
                    difficulty=q["difficulty"],
                    context=q.get("context", "")
                ))
            
            return questions
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
    
    async def _generate_expert_questions(self, transcript: str, topic: str, expert_documents: List[str]) -> List[Question]:
        """Generate expert-level questions based on uploaded documents"""
        
        # Combine document content (simplified - in reality you'd process PDFs)
        document_context = "\n".join(expert_documents[:3])  # Limit to first 3 docs
        
        prompt = f"""
        As an expert in {topic}, generate challenging questions based on both the presentation and these expert documents.
        
        Topic: {topic}
        Presentation: {transcript}
        Expert Documents: {document_context}
        
        Create 5-7 expert-level questions that:
        1. Test deep understanding of the field
        2. Connect presentation content to broader knowledge
        3. Challenge with advanced concepts
        4. Reference specific details from the documents
        
        Format as JSON:
        {{
            "questions": [
                {{
                    "question": "Based on the research in document X, how would you explain...",
                    "category": "expert_analysis",
                    "difficulty": "expert",
                    "context": "Testing expert-level understanding"
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
                            temperature=0.5,
                            max_tokens=1000
                        )
                    resp = await anyio.to_thread.run_sync(_run_hf_chat)
                    content = resp.choices[0].message.content
                else:
                    def _run_hf():
                        return self.hf_client.text_generation(prompt, max_new_tokens=800, temperature=0.5)
                    content = await anyio.to_thread.run_sync(_run_hf)
            else:
                def _run_oa():
                    return self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5
                    )
                response = await anyio.to_thread.run_sync(_run_oa)
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
            questions = []
            for q in result.get("questions", []):
                questions.append(Question(
                    question=q["question"],
                    category=q["category"],
                    difficulty=q["difficulty"],
                    context=q.get("context", "")
                ))
            
            return questions
        except Exception as e:
            print(f"Error generating expert questions: {e}")
            return []

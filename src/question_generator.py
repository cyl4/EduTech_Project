import openai
from typing import List, Dict, Any
from .models import Question, PresentationMode

class QuestionGenerator:
    def __init__(self, openai_client):
        self.client = openai_client
    
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
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
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
            response = await self.client.chat.completions.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
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

# AI Presentation Coach

An AI-powered web application that helps improve presentation skills through real-time analysis and feedback.

## Features

- **Real-time Audio Analysis**: Tracks pace, tone, filler words, intonation, and clarity
- **Content Analysis**: Evaluates clarity, flow, technical accuracy, and explanation quality
- **Adaptive Modes**: Professional, technical, layperson, casual, and custom presentation styles
- **Smart Questions**: AI generates relevant questions to test understanding
- **Improvement Suggestions**: Provides metaphors, analogies, and visual aids for unclear explanations
- **Expert Mode**: Upload PDFs/papers for technical presentations with expert-level questions
- **Comprehensive Scoring**: Detailed feedback with actionable insights

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
# Replace 'your_openai_api_key_here' with your actual OpenAI API key
# Optional: use HuggingFace instead of OpenAI (no OpenAI credits required)
echo "USE_HF=true" >> .env
# Optional: pick a HF chat model (defaults to Llama 3 8B Instruct)
echo "HF_CHAT_MODEL=meta-llama/Meta-Llama-3-8B-Instruct" >> .env
```

3. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## Testing

Run the test script to verify everything is working:
```bash
python test_backend.py
```

This will test all API endpoints, WebSocket connections, and error handling.

## API Endpoints

- `POST /api/sessions` - Create a new presentation session
- `POST /api/sessions/{session_id}/expert-documents` - Upload expert documents
- `GET /api/sessions/{session_id}/summary` - Get session summary
- `DELETE /api/sessions/{session_id}` - Delete a session
- `WebSocket /ws/{session_id}` - Real-time audio analysis

## Usage

1. Create a session with your presentation mode and topic
2. Connect via WebSocket for real-time audio streaming
3. Receive instant feedback on your presentation
4. Get questions and suggestions for improvement
5. View comprehensive scoring and analysis

## Architecture

- **FastAPI**: Web framework with WebSocket support
- **OpenAI**: Speech-to-text and content analysis
- **Librosa**: Audio processing and analysis
- **Pydantic**: Data validation and serialization
- **WebSocket**: Real-time communication

# AI Debate Platform

An interactive platform for practicing debate skills with AI, featuring real-time speech recognition, logical analysis, and AI-powered responses.

## Features

### Core Functionality
- **Real-time Speech Recognition**: Convert your spoken arguments into text using Google Cloud Speech-to-Text
- **Logical Analysis**: Analyze the logical structure and validity of arguments
- **AI Response Generation**: Get intelligent counterarguments from GPT-4
- **Text-to-Speech**: Hear AI responses through high-quality voice synthesis using ElevenLabs
- **Tutorial Mode**: Practice with guided examples to improve logical reasoning

### Technical Features
- FastAPI backend for high performance
- WebSocket support for real-time communication
- Comprehensive error handling and logging
- Modular architecture for easy extension

## Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud account with Speech-to-Text API enabled
- OpenAI API key
- ElevenLabs API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/debate-platform.git
cd debate-platform
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your API keys:
```
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_credentials.json
```

### Running the Application

1. Start the server:
```bash
cd debate_platform
uvicorn app.main:app --reload --port 8001
```

2. Access the API documentation:
```
http://localhost:8001/docs
```

## API Documentation

### Agent Training Endpoints

#### Start a Training Session
```http
POST /agent-training/start
```
Request body:
```json
{
    "topic_id": "ai_ethics",
    "user_side": "supporting"
}
```

#### Submit Audio
```http
POST /agent-training/audio/{conversation_id}
```
Form data:
- `file`: Audio file (WAV format)
- `speaker_id`: User identifier

#### Get Conversation History
```http
GET /agent-training/history/{conversation_id}
```

### Tutorial Endpoints

#### Get Next Question
```http
GET /tutorial/next-question
```

#### Submit Answer
```http
POST /tutorial/answer
```
Form data:
- `question_id`: Integer
- `user_answer`: Boolean

## Project Structure

```
debate_platform/
├── app/
│   ├── api/
│   │   ├── agent_training.py
│   │   ├── debate.py
│   │   └── tutorial.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── llm.py
│   │   ├── logic_chain.py
│   │   ├── stt.py
│   │   └── tts.py
│   └── main.py
├── tests/
│   ├── test_audio.py
│   └── test_logic_chain.py
└── requirements.txt
```

## Development

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI GPT-4 for AI responses
- Google Cloud Speech-to-Text for audio processing
- ElevenLabs for voice synthesis
- FastAPI framework 
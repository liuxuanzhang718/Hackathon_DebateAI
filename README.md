# Debate AI Platform

An intelligent AI-powered debate training platform that helps users improve their debating skills through interactive sessions with an AI agent.

## Features

- 🤖 **AI Debate Agent**: Engage in real-time debates with an intelligent AI agent
- 🧠 **Logic Chain Analysis**: Get detailed analysis of argument structure and validity
- 🗣️ **Speech Processing**: Support for both text and voice interactions
- 📚 **Tutorial System**: Step-by-step guidance for learning debate techniques

## Tech Stack

### Core Technologies
- Python 3.9+
- FastAPI (Web Framework)
- Uvicorn (ASGI Server)

### AI & Machine Learning
- OpenAI API (GPT-4)
- Custom Logic Chain Analysis System

### Speech Processing
- ElevenLabs API (Text-to-Speech)
- Google Cloud Speech-to-Text API

### Development Tools
- Pydantic (Data Validation)
- Python-dotenv (Environment Management)

## Getting Started

### Prerequisites
- Python 3.9 or higher
- API keys for OpenAI, ElevenLabs, and Google Cloud
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/debate-ai-platform.git
cd debate-ai-platform
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application
```bash
uvicorn app.main:app --reload
```

### Running Tests
```bash
pytest
```

## API Documentation

The API documentation is available at `/docs` when running the server.

### Main Endpoints

- `/tutorial/*`: Tutorial system endpoints
- `/agent-training/*`: AI debate training endpoints
- `/debate/*`: Debate session endpoints

For detailed API documentation, see [API.md](API.md).

## Project Structure
```
debate-ai-platform/
├── app/
│   ├── api/         # API endpoints
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   └── main.py      # Application entry
├── tests/           # Test cases
├── audio_storage/   # Audio file storage
└── credentials/     # API credentials
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT API
- ElevenLabs for Text-to-Speech capabilities
- Google Cloud for Speech-to-Text services
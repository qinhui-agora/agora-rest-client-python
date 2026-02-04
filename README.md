# Agora REST Client - Python

Python SDK for Agora REST APIs, including Conversational AI Agent management.

## Features

- 🤖 **High-level Agent API** - Simple interface for managing Agora Conversational AI Agents
- 🔧 **Configuration Management** - Easy configuration from environment variables
- 🎯 **Type-safe** - Full type hints support
- 📦 **Lightweight** - Minimal dependencies
- 🚀 **Production-ready** - Built for reliability and performance

## Installation

### From PyPI (Recommended)

```bash
pip install agora-rest-client-python
```

### From Git Repository

```bash
pip install git+https://github.com/your-org/agora-rest-client-python.git
```

### For Development

```bash
git clone https://github.com/your-org/agora-rest-client-python.git
cd agora-rest-client-python
pip install -e .
```

## Quick Start

### 1. Set up environment variables

Create a `.env` file:

```env
# Agora Configuration
APP_ID=your_app_id
APP_CERTIFICATE=your_app_certificate

# Agora REST API Credentials
API_KEY=your_customer_id
API_SECRET=your_customer_secret

# LLM - OpenAI
LLM_API_KEY=your_openai_key

# ASR - Deepgram (Optional)
ASR_DEEPGRAM_API_KEY=your_deepgram_key

# TTS - ElevenLabs (Optional)
TTS_ELEVENLABS_API_KEY=your_elevenlabs_key
```

### 2. Initialize and use the Agent

```python
import os
from agora_rest import AgentClient
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig

# Create agent client
client = AgentClient(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    customer_id=os.getenv("API_KEY"),
    customer_secret=os.getenv("API_SECRET")
)

# Generate connection configuration
config_data = client.generate_config()
print(f"Channel: {config_data['channel_name']}")
print(f"Token: {config_data['token']}")

# Configure ASR, LLM, TTS
asr = DeepgramASRConfig(api_key=os.getenv("ASR_DEEPGRAM_API_KEY"))
llm = OpenAILLMConfig(api_key=os.getenv("LLM_API_KEY"))
tts = ElevenLabsTTSConfig(api_key=os.getenv("TTS_ELEVENLABS_API_KEY"))

# Start an agent
result = client.start_agent(
    channel_name=config_data['channel_name'],
    agent_uid=config_data['agent_uid'],
    user_uid=config_data['uid'],
    asr_config=asr,
    llm_config=llm,
    tts_config=tts
)

print(f"Agent started: {result['agent_id']}")


# Stop the agent
manager.stop_agent(result['agent_id'])
print("Agent stopped")
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `APP_ID` | Agora App ID | Yes |
| `APP_CERTIFICATE` | Agora App Certificate | Yes |
| `API_KEY` | Agora REST API Customer ID | Yes |
| `API_SECRET` | Agora REST API Customer Secret | Yes |
| `LLM_API_KEY` | OpenAI LLM API key | Yes |
| `ASR_DEEPGRAM_API_KEY` | Deepgram ASR API key | Optional |
| `TTS_ELEVENLABS_API_KEY` | ElevenLabs TTS API key | Optional |
| `PORT` | Server port (default: 8000) | Optional |

## API Reference

### AgentClient

Core business logic for agent operations.

```python
import os
from agora_rest import AgentClient

client = AgentClient(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    customer_id=os.getenv("API_KEY"),
    customer_secret=os.getenv("API_SECRET")
)

# Generate connection configuration
config_data = client.generate_config()

# Start an agent
result = manager.start_agent(
    channel_name="my_channel",
    agent_uid="123",
    user_uid="456",
    asr_config={...},
    llm_config={...},
    tts_config={...}
)

# Stop an agent
manager.stop_agent(agent_id)
```

### Configuration Components

```python
from agora_rest.agent import ASRConfig, LLMConfig, TTSConfig

# ASR Configuration (Deepgram) - uses defaults
asr = ASRConfig(api_key="your_deepgram_key")

# LLM Configuration (OpenAI) - uses defaults
llm = LLMConfig(api_key="your_openai_key")

# TTS Configuration (ElevenLabs) - uses defaults
tts = TTSConfig(api_key="your_elevenlabs_key")

# Optional: Customize if needed
# llm.model = "gpt-4o"
# llm.system_message = "You are a helpful assistant"
# asr.language = "zh-CN"
```

## Supported Vendors

### ASR (Automatic Speech Recognition)
- ✅ Deepgram

### LLM (Large Language Model)
- ✅ OpenAI (GPT-4, GPT-3.5)

### TTS (Text-to-Speech)
- ✅ ElevenLabs

## Examples

See the [examples](examples/) directory for more usage examples.

## Requirements

- Python >= 3.8
- Dependencies listed in [requirements.txt](requirements.txt)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/your-org/agora-rest-client-python.git
cd agora-rest-client-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .
```

### Running Tests

```bash
pytest
```

### Code Style

```bash
# Format code
black .

# Lint code
flake8 .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@agora.io
- 📖 Documentation: [Agora Docs](https://docs.agora.io)
- 💬 Community: [Agora Community](https://www.agora.io/en/community/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

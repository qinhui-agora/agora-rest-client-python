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
import uuid
import random
from agora_rest.agent import (
    AgentClient,
    TokenBuilder,
    DeepgramASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig
)

# Create agent client
client = AgentClient(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    customer_id=os.getenv("API_KEY"),
    customer_secret=os.getenv("API_SECRET")
)

# Generate connection configuration
channel_name = f"channel_{uuid.uuid4().hex[:8]}"
user_uid = str(random.randint(100000, 999999))
agent_uid = str(random.randint(100000, 999999))

token = TokenBuilder.generate(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    channel_name=channel_name,
    uid=agent_uid
)

print(f"Channel: {channel_name}")
print(f"Token: {token}")

# Configure ASR, LLM, TTS - simple, only required fields
asr = DeepgramASRConfig(api_key=os.getenv("ASR_DEEPGRAM_API_KEY"))
llm = OpenAILLMConfig(api_key=os.getenv("LLM_API_KEY"))
tts = ElevenLabsTTSConfig(api_key=os.getenv("TTS_ELEVENLABS_API_KEY"))

# Optional: Customize configurations
# asr.language = "zh-CN"
# llm.model = "gpt-4o"
# tts.voice_id = "custom_voice_id"

# Alternative: Use dictionaries
# asr = {"vendor": "deepgram", "api_key": "xxx", "language": "zh-CN"}
# llm = {"api_key": "xxx", "model": "gpt-4o"}
# tts = {"vendor": "elevenlabs", "api_key": "xxx"}

# Advanced: Use custom vendors (Azure, Google, etc.)
# asr = {"vendor": "azure", "params": {"subscription_key": "xxx", "region": "eastus"}}
# tts = {"vendor": "azure", "params": {"subscription_key": "xxx", "voice_name": "zh-CN-XiaoxiaoNeural"}}

# Start an agent
result = client.start_agent(
    channel_name=channel_name,
    agent_uid=agent_uid,
    user_uid=user_uid,
    asr_config=asr,
    llm_config=llm,
    tts_config=tts
)

print(f"Agent started: {result['agent_id']}")

# Stop the agent
client.stop_agent(result['agent_id'])
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
import uuid
import random
from agora_rest.agent import AgentClient, TokenBuilder

client = AgentClient(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    customer_id=os.getenv("API_KEY"),
    customer_secret=os.getenv("API_SECRET")
)

# Generate connection configuration
channel_name = f"channel_{uuid.uuid4().hex[:8]}"
user_uid = str(random.randint(100000, 999999))
agent_uid = str(random.randint(100000, 999999))

token = TokenBuilder.generate(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    channel_name=channel_name,
    uid=agent_uid
)

# Start an agent
result = client.start_agent(
    channel_name=channel_name,
    agent_uid=agent_uid,
    user_uid=user_uid,
    asr_config={...},
    llm_config={...},
    tts_config={...}
)

# Stop an agent
client.stop_agent(agent_id)
```

### Configuration Components

```python
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig

# ASR Configuration (Deepgram) - simple, only api_key required
asr = DeepgramASRConfig(api_key="your_deepgram_key")
# Optional: customize with defaults
# asr.language = "zh-CN"
# asr.model = "nova-3"

# LLM Configuration (OpenAI) - simple, only api_key required
llm = OpenAILLMConfig(api_key="your_openai_key")
# Optional: customize
# llm.model = "gpt-4o"
# llm.system_message = "You are a helpful assistant"
# llm.max_tokens = 512

# TTS Configuration (ElevenLabs) - simple, only api_key required
tts = ElevenLabsTTSConfig(api_key="your_elevenlabs_key")
# Optional: customize
# tts.voice_id = "custom_voice_id"
# tts.stability = 0.5
```

## Supported Vendors

### Built-in Vendors (Configuration Classes Provided)

All built-in vendors have dedicated configuration classes for easy use.

#### ASR (Automatic Speech Recognition)
- ✅ **Deepgram** - `DeepgramASRConfig` (Recommended for English)
- ✅ **Fengming** - `FengmingASRConfig`
- ✅ **Tencent** - `TencentASRConfig`
- ✅ **Microsoft** - `MicrosoftASRConfig` (Azure Speech)
- ✅ **Ares** - `AresASRConfig`

#### LLM (Large Language Model)
- ✅ **OpenAI** - `OpenAILLMConfig` (GPT-4, GPT-3.5, GPT-4o)
- ✅ **Azure OpenAI** - Use `OpenAILLMConfig` (Compatible with OpenAI API)
- ✅ **Any OpenAI-compatible API** - Use `OpenAILLMConfig`

#### TTS (Text-to-Speech)
- ✅ **ElevenLabs** - `ElevenLabsTTSConfig` (Recommended for quality)
- ✅ **Minimax** - `MinimaxTTSConfig`
- ✅ **Tencent** - `TencentTTSConfig`
- ✅ **Bytedance** - `BytedanceTTSConfig`
- ✅ **Microsoft** - `MicrosoftTTSConfig` (Azure TTS)
- ✅ **Cartesia** - `CartesiaTTSConfig`
- ✅ **OpenAI** - `OpenAITTSConfig` (OpenAI TTS)

### Usage Examples

#### Using Built-in Vendors (Simple)

```python
from agora_rest.agent import (
    DeepgramASRConfig,
    MicrosoftASRConfig,
    TencentASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig,
    MicrosoftTTSConfig,
    OpenAITTSConfig,
)

# ASR - Deepgram (English) - simple, only api_key required
asr = DeepgramASRConfig(api_key="xxx")
# Optional: customize
# asr.language = "zh-CN"
# asr.model = "nova-3"

# ASR - Microsoft (Chinese)
asr = MicrosoftASRConfig(key="xxx", language="zh-CN")

# ASR - Tencent
asr = TencentASRConfig(
    key="xxx",
    app_id="xxx",
    secret="xxx"
)

# LLM - OpenAI
llm = OpenAILLMConfig(api_key="xxx")
# Optional: customize
# llm.model = "gpt-4o"

# TTS - ElevenLabs - simple, only api_key required
tts = ElevenLabsTTSConfig(api_key="xxx")
# Optional: customize
# tts.voice_id = "custom_voice_id"

# TTS - Microsoft (Chinese voice)
tts = MicrosoftTTSConfig(
    key="xxx",
    voice_name="zh-CN-XiaoxiaoNeural"
)

# TTS - OpenAI
tts = OpenAITTSConfig(api_key="xxx")
# Optional: customize
# tts.model = "tts-1-hd"
# tts.voice = "nova"
```

#### Using Custom Vendors (Advanced)

For vendors not listed above, use dictionary with `params`:

```python
# Example: Custom ASR vendor
asr = {
    "vendor": "custom_asr",
    "params": {
        "api_key": "xxx",
        "custom_param": "value"
    }
}

# Example: Custom TTS vendor
tts = {
    "vendor": "custom_tts",
    "params": {
        "api_key": "xxx",
        "custom_param": "value"
    }
}

client.start_agent(..., asr_config=asr, tts_config=tts)
```

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

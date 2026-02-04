# Agora REST Client Python Examples

This directory contains examples demonstrating different ways to use the Agora REST Client Python SDK.

## Directory Structure

```
examples/
├── README.md                    # This file
├── high_level_api/
│   └── basic_usage.py          # High-level API example
└── low_level_api/
    └── basic_usage.py          # Low-level API example
```

## Quick Start

### High-Level API (Recommended for beginners)

```bash
python examples/high_level_api/basic_usage.py
```

### Low-Level API (For advanced control)

```bash
python examples/low_level_api/basic_usage.py
```

## API Overview

### 1. High-Level API

**Location:** `high_level_api/basic_usage.py`

The high-level API provides a simplified interface through the `AgentClient` class.

**Features:**
- Automatic configuration management
- Built-in token generation
- Simplified agent lifecycle management
- Easy-to-use configuration classes (ASRConfig, LLMConfig, TTSConfig)

**Example:**
```python
import os
from agora_rest import AgentClient
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig

# Create client
client = AgentClient(
    app_id=os.getenv("APP_ID"),
    app_certificate=os.getenv("APP_CERTIFICATE"),
    customer_id=os.getenv("API_KEY"),
    customer_secret=os.getenv("API_SECRET")
)

# Generate connection config (token, channel, UIDs)
config_data = manager.generate_config()

# Configure components with API keys (uses defaults for other settings)
asr = ASRConfig(api_key=config.deepgram_api_key)
llm = LLMConfig(api_key=config.llm_api_key)
tts = TTSConfig(api_key=config.tts_elevenlabs_api_key)

# Optional: Customize if needed
# llm.model = "gpt-4o"
# llm.system_message = "You are a helpful AI assistant."

# Start agent
result = manager.start_agent(
    channel_name=config_data['channel_name'],
    agent_uid=config_data['agent_uid'],
    user_uid=config_data['uid'],
    asr_config=asr.to_dict(),
    llm_config=llm.to_dict(),
    tts_config=tts.to_dict()
)

# Stop agent
manager.stop_agent(result['agent_id'])
```

### 2. Low-Level API

**Location:** `low_level_api/basic_usage.py`

The low-level API provides direct access to the REST client through the `ConvoAIClient` class, giving you full control over API calls and configurations.

**Features:**
- Direct control over all API parameters
- Access to all request/response models
- Fine-grained configuration options
- Support for multiple TTS providers

**Example:**
```python
from agora_rest import ConvoAIClient, Config, ServiceRegion, BasicAuthCredential
from agora_rest.req.join import (
    JoinPropertiesReqBody,
    JoinPropertiesCustomLLMBody,
    JoinPropertiesTTSBody,
    TTSVendor,
    TTSElevenLabsVendorParams
)

# Create client
credential = BasicAuthCredential(api_key, api_secret)
config = Config(
    app_id=app_id,
    credential=credential,
    service_region=ServiceRegion.GLOBAL
)
client = ConvoAIClient(config)

# Configure LLM
llm_config = JoinPropertiesCustomLLMBody(
    url="https://api.openai.com/v1/chat/completions",
    api_key=llm_api_key,
    system_messages=[{"role": "system", "content": "You are helpful."}],
    params={"model": "gpt-4", "max_tokens": 1024}
)

# Configure TTS
tts_config = JoinPropertiesTTSBody(
    vendor=TTSVendor.ELEVENLABS,
    params=TTSElevenLabsVendorParams(
        key=tts_api_key,
        model_id="eleven_multilingual_v2",
        voice_id="pNInz6obpgDQGcFmaJgB"
    )
)

# Create join properties
properties = JoinPropertiesReqBody(
    token=rtc_token,
    channel=channel,
    agent_rtc_uid=agent_uid,
    remote_rtc_uids=[user_uid],
    llm=llm_config,
    tts=tts_config
)

# Join - create agent
join_resp = client.join(name="my_agent", properties=properties)
agent_id = join_resp.success_resp.agent_id

# Leave - stop agent
leave_resp = client.leave(agent_id)
```

## Environment Variables

Create a `.env` file in the project root:

### For High-Level API

```bash
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

### For Low-Level API

```bash
# Agora Configuration
APP_ID=your_app_id
API_KEY=your_customer_id
API_SECRET=your_customer_secret

# RTC Configuration
RTC_TOKEN=your_rtc_token
CHANNEL=test_channel
AGENT_UID=123456
USER_UID=789012

# LLM - OpenAI
LLM_API_KEY=your_openai_key

# TTS - ElevenLabs
TTS_ELEVENLABS_API_KEY=your_elevenlabs_key

# ASR - Deepgram (Optional)
ASR_DEEPGRAM_API_KEY=your_deepgram_key
```

## Additional Resources

- [Agora Conversational AI Documentation](https://docs.agora.io/en/conversational-ai/overview)
- [API Reference](https://docs.agora.io/en/conversational-ai/reference/api)

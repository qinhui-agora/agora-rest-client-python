"""
Agent Components

Configuration objects for ASR, LLM, and TTS components.

Supported vendors:
- ASR: Deepgram
- LLM: OpenAI
- TTS: ElevenLabs
"""
from typing import Optional
from dataclasses import dataclass, field


# Default configurations
DEFAULT_DEEPGRAM_URL = "wss://api.deepgram.com/v1/listen"
DEFAULT_DEEPGRAM_MODEL = "nova-2"
DEFAULT_DEEPGRAM_LANGUAGE = "en-US"

DEFAULT_OPENAI_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4"
DEFAULT_OPENAI_MAX_TOKENS = 1024
DEFAULT_OPENAI_MAX_HISTORY = 64
DEFAULT_OPENAI_SYSTEM_MESSAGE = "You are a helpful assistant."
DEFAULT_OPENAI_GREETING = "Hello, how can I help you?"

DEFAULT_ELEVENLABS_MODEL = "eleven_multilingual_v2"
DEFAULT_ELEVENLABS_VOICE = "pNInz6obpgDQGcFmaJgB"


@dataclass
class ASRConfig:
    """ASR (Automatic Speech Recognition) Configuration - Deepgram"""
    vendor: str = "deepgram"
    api_key: Optional[str] = None
    url: str = DEFAULT_DEEPGRAM_URL
    model: str = DEFAULT_DEEPGRAM_MODEL
    language: str = DEFAULT_DEEPGRAM_LANGUAGE
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "vendor": self.vendor,
            "api_key": self.api_key,
            "url": self.url,
            "model": self.model,
            "language": self.language
        }


@dataclass
class LLMConfig:
    """LLM (Large Language Model) Configuration - OpenAI"""
    url: str = DEFAULT_OPENAI_URL
    api_key: str = ""
    model: str = DEFAULT_OPENAI_MODEL
    max_tokens: int = DEFAULT_OPENAI_MAX_TOKENS
    max_history: int = DEFAULT_OPENAI_MAX_HISTORY
    system_message: str = DEFAULT_OPENAI_SYSTEM_MESSAGE
    greeting: str = DEFAULT_OPENAI_GREETING
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "url": self.url,
            "api_key": self.api_key,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "max_history": self.max_history,
            "system_message": self.system_message,
            "greeting": self.greeting
        }


@dataclass
class TTSConfig:
    """TTS (Text-to-Speech) Configuration - ElevenLabs"""
    vendor: str = "elevenlabs"
    api_key: Optional[str] = None
    model_id: str = DEFAULT_ELEVENLABS_MODEL
    voice_id: str = DEFAULT_ELEVENLABS_VOICE
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "vendor": self.vendor,
            "api_key": self.api_key,
            "model_id": self.model_id,
            "voice_id": self.voice_id
        }

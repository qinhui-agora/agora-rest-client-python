"""
Agent Components

Configuration objects for ASR, LLM, and TTS components.

Supported vendors:
- ASR: Deepgram
- LLM: OpenAI
- TTS: ElevenLabs

Users can create custom configurations by inheriting from base classes.
"""
from typing import Optional, Dict, Any, Protocol
from dataclasses import dataclass, field


# Configuration Protocol
class ConfigProtocol(Protocol):
    """Protocol that all config classes should implement"""
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        ...


# Base Classes
@dataclass
class BaseASRConfig:
    """Base class for ASR configurations"""
    vendor: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering out None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class BaseLLMConfig:
    """Base class for LLM configurations"""
    api_key: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering out None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class BaseTTSConfig:
    """Base class for TTS configurations"""
    vendor: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering out None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


# Deepgram ASR Configuration
@dataclass
class DeepgramASRConfig(BaseASRConfig):
    """Deepgram ASR Configuration"""
    vendor: str = "deepgram"
    api_key: Optional[str] = None
    url: str = "wss://api.deepgram.com/v1/listen"
    model: str = "nova-2"
    language: str = "en-US"


# OpenAI LLM Configuration
@dataclass
class OpenAILLMConfig(BaseLLMConfig):
    """OpenAI LLM Configuration"""
    api_key: str = ""
    url: str = "https://api.openai.com/v1"
    model: str = "gpt-4"
    max_tokens: int = 1024
    max_history: int = 64
    system_message: str = "You are a helpful assistant."
    greeting: str = "Hello, how can I help you?"


# ElevenLabs TTS Configuration
@dataclass
class ElevenLabsTTSConfig(BaseTTSConfig):
    """ElevenLabs TTS Configuration"""
    vendor: str = "elevenlabs"
    api_key: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    voice_id: str = "pNInz6obpgDQGcFmaJgB"


# Backward compatibility aliases
ASRConfig = DeepgramASRConfig
LLMConfig = OpenAILLMConfig
TTSConfig = ElevenLabsTTSConfig

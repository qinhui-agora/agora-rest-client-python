"""
Agent - High-level API for Agora Conversational AI Agents

Main classes:
- AgentClient: Core business logic handler
- DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig: Vendor-specific configurations
- BaseASRConfig, BaseLLMConfig, BaseTTSConfig: Base classes for custom configurations
- ASRConfig, LLMConfig, TTSConfig: Backward compatibility aliases
- TokenBuilder: Token generation utility
- PropertyBuilder: Property building utility
"""

from .components import (
    # Base classes
    BaseASRConfig,
    BaseLLMConfig,
    BaseTTSConfig,
    # Vendor-specific configs
    DeepgramASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig,
    # Backward compatibility
    ASRConfig,
    LLMConfig,
    TTSConfig,
)
from .client import AgentClient
from .token import TokenBuilder
from .property import PropertyBuilder

__all__ = [
    "AgentClient",
    # Base classes
    "BaseASRConfig",
    "BaseLLMConfig",
    "BaseTTSConfig",
    # Vendor-specific configs
    "DeepgramASRConfig",
    "OpenAILLMConfig",
    "ElevenLabsTTSConfig",
    # Backward compatibility
    "ASRConfig",
    "LLMConfig",
    "TTSConfig",
    # Utilities
    "TokenBuilder",
    "PropertyBuilder",
]

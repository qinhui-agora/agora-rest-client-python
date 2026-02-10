"""
Agent Components

Configuration objects for ASR, LLM, and TTS components.

This module provides user-friendly wrapper classes with sensible defaults.
Internally, these classes use Pydantic models from agora_rest.req.join for validation.

Supported vendors:
- ASR: Deepgram, Fengming, Tencent, Microsoft, Ares
- LLM: OpenAI (and compatible APIs)
- TTS: ElevenLabs, Minimax, Tencent, Bytedance, Microsoft, Cartesia, OpenAI

Users can create custom configurations by:
1. Using built-in config classes for supported vendors (recommended)
2. Passing dictionaries with custom 'params' for other vendors
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Import Pydantic models from join.py (used internally)
from ..req.join import (
    ASRDeepgramVendorParam,
    ASRFengmingVendorParam,
    ASRTencentVendorParam,
    ASRMicrosoftVendorParam,
    ASRAresVendorParam,
    TTSElevenLabsVendorParams,
    TTSMinimaxVendorParams,
    TTSTencentVendorParams,
    TTSBytedanceVendorParams,
    TTSMicrosoftVendorParams,
    TTSCartesiaVendorParams,
    TTSOpenAIVendorParams,
)


# ============================================================================
# ASR (Automatic Speech Recognition) Configurations
# ============================================================================

@dataclass
class DeepgramASRConfig:
    """Deepgram ASR Configuration - user-friendly wrapper with defaults"""
    api_key: str
    url: str = "wss://api.deepgram.com/v1/listen"
    model: str = "nova-2"
    language: str = "en-US"
    
    def to_pydantic(self) -> ASRDeepgramVendorParam:
        """Convert to Pydantic model for internal use"""
        return ASRDeepgramVendorParam(
            url=self.url,
            key=self.api_key,
            model=self.model,
            language=self.language
        )


@dataclass
class FengmingASRConfig:
    """Fengming ASR Configuration"""
    
    def to_pydantic(self) -> ASRFengmingVendorParam:
        """Convert to Pydantic model for internal use"""
        return ASRFengmingVendorParam()


@dataclass
class TencentASRConfig:
    """Tencent ASR Configuration"""
    key: str
    app_id: str
    secret: str
    engine_model_type: str = "16k_zh"
    voice_id: str = ""
    
    def to_pydantic(self) -> ASRTencentVendorParam:
        """Convert to Pydantic model for internal use"""
        return ASRTencentVendorParam(
            key=self.key,
            app_id=self.app_id,
            secret=self.secret,
            engine_model_type=self.engine_model_type,
            voice_id=self.voice_id
        )


@dataclass
class MicrosoftASRConfig:
    """Microsoft ASR Configuration"""
    key: str
    region: str = "eastus"
    language: str = "en-US"
    phrase_list: List[str] = None
    
    def __post_init__(self):
        if self.phrase_list is None:
            self.phrase_list = []
    
    def to_pydantic(self) -> ASRMicrosoftVendorParam:
        """Convert to Pydantic model for internal use"""
        return ASRMicrosoftVendorParam(
            key=self.key,
            region=self.region,
            language=self.language,
            phrase_list=self.phrase_list
        )


@dataclass
class AresASRConfig:
    """Ares ASR Configuration"""
    
    def to_pydantic(self) -> ASRAresVendorParam:
        """Convert to Pydantic model for internal use"""
        return ASRAresVendorParam()


# ============================================================================
# LLM (Large Language Model) Configuration
# ============================================================================

@dataclass
class OpenAILLMConfig:
    """OpenAI LLM Configuration (also compatible with Azure OpenAI and other OpenAI-compatible APIs)"""
    api_key: str
    url: str = "https://api.openai.com/v1"
    model: str = "gpt-4"
    max_tokens: int = 1024
    max_history: int = 64
    system_message: str = "You are a helpful assistant."
    greeting: str = "Hello, how can I help you?"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering out None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


# ============================================================================
# TTS (Text-to-Speech) Configurations
# ============================================================================

@dataclass
class ElevenLabsTTSConfig:
    """ElevenLabs TTS Configuration - user-friendly wrapper with defaults"""
    api_key: str
    model_id: str = "eleven_multilingual_v2"
    voice_id: str = "pNInz6obpgDQGcFmaJgB"
    sample_rate: Optional[int] = 24000
    stability: Optional[float] = None
    similarity_boost: Optional[float] = None
    style: Optional[float] = None
    use_speaker_boost: Optional[bool] = None
    
    def to_pydantic(self) -> TTSElevenLabsVendorParams:
        """Convert to Pydantic model for internal use"""
        return TTSElevenLabsVendorParams(
            key=self.api_key,
            model_id=self.model_id,
            voice_id=self.voice_id,
            sample_rate=self.sample_rate,
            stability=self.stability,
            similarity_boost=self.similarity_boost,
            style=self.style,
            use_speaker_boost=self.use_speaker_boost
        )


@dataclass
class MinimaxTTSConfig:
    """Minimax TTS Configuration"""
    group_id: str
    key: str
    model: str
    voice_id: str = ""
    speed: float = 1.0
    vol: float = 1.0
    pitch: int = 0
    emotion: str = "neutral"
    sample_rate: int = 24000
    url: Optional[str] = None
    
    def to_pydantic(self) -> TTSMinimaxVendorParams:
        """Convert to Pydantic model for internal use"""
        from ..req.join import TTSMinimaxVendorVoiceSettingParam, TTSMinimaxVendorAudioSettingParam
        
        voice_setting = TTSMinimaxVendorVoiceSettingParam(
            voice_id=self.voice_id,
            speed=self.speed,
            vol=self.vol,
            pitch=self.pitch,
            emotion=self.emotion
        )
        
        audio_setting = TTSMinimaxVendorAudioSettingParam(
            sample_rate=self.sample_rate
        )
        
        return TTSMinimaxVendorParams(
            group_id=self.group_id,
            key=self.key,
            model=self.model,
            voice_setting=voice_setting,
            audio_setting=audio_setting,
            url=self.url
        )


@dataclass
class TencentTTSConfig:
    """Tencent TTS Configuration"""
    app_id: str
    secret_id: str
    secret_key: str
    voice_type: int = 0
    volume: int = 0
    speed: int = 0
    emotion_category: str = ""
    emotion_intensity: int = 0
    
    def to_pydantic(self) -> TTSTencentVendorParams:
        """Convert to Pydantic model for internal use"""
        return TTSTencentVendorParams(
            app_id=self.app_id,
            secret_id=self.secret_id,
            secret_key=self.secret_key,
            voice_type=self.voice_type,
            volume=self.volume,
            speed=self.speed,
            emotion_category=self.emotion_category,
            emotion_intensity=self.emotion_intensity
        )


@dataclass
class BytedanceTTSConfig:
    """Bytedance TTS Configuration"""
    token: str
    app_id: str
    cluster: str
    voice_type: str
    speed_ratio: float = 1.0
    volume_ratio: float = 1.0
    pitch_ratio: float = 1.0
    emotion: str = ""
    
    def to_pydantic(self) -> TTSBytedanceVendorParams:
        """Convert to Pydantic model for internal use"""
        return TTSBytedanceVendorParams(
            token=self.token,
            app_id=self.app_id,
            cluster=self.cluster,
            voice_type=self.voice_type,
            speed_ratio=self.speed_ratio,
            volume_ratio=self.volume_ratio,
            pitch_ratio=self.pitch_ratio,
            emotion=self.emotion
        )


@dataclass
class MicrosoftTTSConfig:
    """Microsoft TTS Configuration"""
    key: str
    region: str = "eastus"
    voice_name: str = "en-US-JennyNeural"
    speed: float = 1.0
    volume: float = 100.0
    sample_rate: int = 24000
    
    def to_pydantic(self) -> TTSMicrosoftVendorParams:
        """Convert to Pydantic model for internal use"""
        return TTSMicrosoftVendorParams(
            key=self.key,
            region=self.region,
            voice_name=self.voice_name,
            speed=self.speed,
            volume=self.volume,
            sample_rate=self.sample_rate
        )


@dataclass
class CartesiaTTSConfig:
    """Cartesia TTS Configuration"""
    api_key: str
    model_id: str
    voice_mode: str = "id"
    voice_id: str = ""
    
    def to_pydantic(self) -> TTSCartesiaVendorParams:
        """Convert to Pydantic model for internal use"""
        from ..req.join import TTSCartesiaVendorVoice
        
        voice = None
        if self.voice_id:
            voice = TTSCartesiaVendorVoice(
                mode=self.voice_mode,
                id=self.voice_id
            )
        
        return TTSCartesiaVendorParams(
            api_key=self.api_key,
            model_id=self.model_id,
            voice=voice
        )


@dataclass
class OpenAITTSConfig:
    """OpenAI TTS Configuration"""
    api_key: str
    model: str = "tts-1"
    voice: str = "alloy"
    instructions: str = ""
    speed: float = 1.0
    
    def to_pydantic(self) -> TTSOpenAIVendorParams:
        """Convert to Pydantic model for internal use"""
        return TTSOpenAIVendorParams(
            api_key=self.api_key,
            model=self.model,
            voice=self.voice,
            instructions=self.instructions,
            speed=self.speed
        )


# ============================================================================
# Backward Compatibility Aliases
# ============================================================================

# Keep old names for backward compatibility
ASRConfig = DeepgramASRConfig
LLMConfig = OpenAILLMConfig
TTSConfig = ElevenLabsTTSConfig

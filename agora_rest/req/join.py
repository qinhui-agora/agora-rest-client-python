"""
Join API request models

Corresponds to Go version: agora-rest-client-go/services/convoai/req/join.go

This file implements the complete request models for the Join API, including:
- TTS (Text-to-Speech) configurations for multiple vendors
- ASR (Automatic Speech Recognition) configurations
- LLM (Large Language Model) configurations
- MLLM (Multimodal Large Language Model) configurations
- Advanced features and parameters

@since v0.7.0
"""
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# TTS (Text-to-Speech) Models
# ============================================================================

class TTSVendor(str, Enum):
    """
    TTS vendor enumeration
    
    @since v0.7.0
    """
    MINIMAX = "minimax"
    TENCENT = "tencent"
    BYTEDANCE = "bytedance"
    MICROSOFT = "microsoft"
    ELEVENLABS = "elevenlabs"  # Note: Go uses "elevenLabs" with capital L
    CARTESIA = "cartesia"  # @since v0.12.0
    OPENAI = "openai"  # @since v0.12.0


# TTS Vendor Parameters

class TTSMinimaxVendorVoiceSettingParam(BaseModel):
    """Minimax TTS voice setting parameters"""
    voice_id: str
    speed: float
    vol: float
    pitch: int
    emotion: str
    latex_render: Optional[bool] = None
    english_normalization: Optional[bool] = None


class TTSMinimaxVendorAudioSettingParam(BaseModel):
    """Minimax TTS audio setting parameters"""
    sample_rate: int


class PronunciationDictParam(BaseModel):
    """Pronunciation dictionary parameters"""
    tone: List[str]


class TimberWeightsParam(BaseModel):
    """Timber weights parameters"""
    voice_id: str
    weight: int


class TTSMinimaxVendorParams(BaseModel):
    """
    Minimax vendor parameters for the Text-to-Speech (TTS) module
    
    See https://platform.minimaxi.com/document/T2A%20V2 for details
    
    @since v0.7.0
    """
    group_id: str
    key: str
    model: str
    voice_setting: Optional[TTSMinimaxVendorVoiceSettingParam] = None
    audio_setting: Optional[TTSMinimaxVendorAudioSettingParam] = None
    pronunciation_dict: Optional[PronunciationDictParam] = None
    timber_weights: Optional[List[TimberWeightsParam]] = None
    url: Optional[str] = Field(
        None,
        description="WebSocket endpoint URL for MiniMax TTS (e.g., wss://api.minimax.io/ws/v1/t2a_v2)"
    )


class TTSTencentVendorParams(BaseModel):
    """
    Tencent vendor parameters for the Text-to-Speech (TTS) module
    
    See https://cloud.tencent.com/document/product/1073/94308 for details
    
    @since v0.7.0
    """
    app_id: str
    secret_id: str
    secret_key: str
    voice_type: int
    volume: int
    speed: int
    emotion_category: str
    emotion_intensity: int


class TTSBytedanceVendorParams(BaseModel):
    """
    Bytedance vendor parameters for the Text-to-Speech (TTS) module
    
    See https://www.volcengine.com/docs/6561/79823 for details
    
    @since v0.7.0
    """
    token: str
    app_id: str
    cluster: str
    voice_type: str
    speed_ratio: float
    volume_ratio: float
    pitch_ratio: float
    emotion: str


class TTSMicrosoftVendorParams(BaseModel):
    """
    Microsoft vendor parameters for the Text-to-Speech (TTS) module
    
    @since v0.12.0
    """
    key: str = Field(..., description="The API key used for authentication (Required)")
    region: str = Field(..., description="The Azure region where the speech service is hosted (Required)")
    voice_name: str = Field(..., description="The identifier for the selected voice for speech synthesis (Optional)")
    speed: float = Field(..., description="Speaking rate of the text, between 0.5 and 2.0 (Optional)")
    volume: float = Field(..., description="Audio volume between 0.0 and 100.0 (Optional)")
    sample_rate: int = Field(default=24000, description="Audio sampling rate in Hz (Optional)")


class TTSElevenLabsVendorParams(BaseModel):
    """
    ElevenLabs vendor parameters for the Text-to-Speech (TTS) module
    
    @since v0.12.0
    """
    key: str = Field(..., description="The API key used for authentication (Required)")
    model_id: str = Field(..., description="Identifier of the model to be used (Required)")
    voice_id: str = Field(..., description="The identifier for the selected voice (Required)")
    sample_rate: Optional[int] = Field(default=24000, description="Audio sampling rate in Hz (Optional)")
    stability: Optional[float] = Field(None, description="The stability for voice settings (Optional)")
    similarity_boost: Optional[float] = Field(None, description="How closely the AI should adhere to the original voice")
    style: Optional[float] = Field(None, description="Style exaggeration of the voice")
    use_speaker_boost: Optional[bool] = Field(None, description="Boosts similarity to the original speaker")


class TTSCartesiaVendorVoice(BaseModel):
    """
    Cartesia vendor voice configuration
    
    @since v0.12.0
    """
    mode: str
    id: str


class TTSCartesiaVendorParams(BaseModel):
    """
    Cartesia vendor parameters for the Text-to-Speech (TTS) module
    
    @since v0.12.0
    """
    api_key: str
    model_id: str
    voice: Optional[TTSCartesiaVendorVoice] = None


class TTSOpenAIVendorParams(BaseModel):
    """
    OpenAI vendor parameters for the Text-to-Speech (TTS) module
    
    @since v0.12.0
    """
    api_key: str
    model: str
    voice: str
    instructions: str
    speed: float


# Union type for all TTS vendor parameters
TTSVendorParams = Union[
    TTSMinimaxVendorParams,
    TTSTencentVendorParams,
    TTSBytedanceVendorParams,
    TTSMicrosoftVendorParams,
    TTSElevenLabsVendorParams,
    TTSCartesiaVendorParams,
    TTSOpenAIVendorParams,
]


class JoinPropertiesTTSBody(BaseModel):
    """
    Text-to-Speech (TTS) module configuration for the agent to join the RTC channel
    
    @since v0.7.0
    """
    vendor: TTSVendor = Field(..., description="TTS vendor")
    params: TTSVendorParams = Field(..., description="TTS vendor parameter description")
    skip_patterns: Optional[List[int]] = Field(
        None,
        description="""Controls whether the TTS module skips bracketed content when reading LLM response text.
        
        Enable this feature by specifying one or more values:
        1: Skip content in Chinese parentheses （ ）
        2: Skip content in Chinese square brackets 【】
        3: Skip content in parentheses ()
        4: Skip content in square brackets [ ]
        5: Skip content in curly braces { }
        
        @since v0.12.0
        """
    )


# ============================================================================
# ASR (Automatic Speech Recognition) Models
# ============================================================================

class ASRVendor(str, Enum):
    """
    ASR vendor enumeration
    
    @since v0.12.0
    """
    FENGMING = "fengming"
    TENCENT = "tencent"
    MICROSOFT = "microsoft"
    ARES = "ares"
    DEEPGRAM = "deepgram"


class ASRFengmingVendorParam(BaseModel):
    """
    Fengming ASR vendor parameter
    
    @since v0.12.0
    """
    pass  # No parameters required


class ASRAresVendorParam(BaseModel):
    """
    Ares ASR vendor parameter
    
    @since v0.12.0
    """
    pass  # No parameters required


class ASRTencentVendorParam(BaseModel):
    """
    Tencent ASR vendor parameter
    
    @since v0.12.0
    """
    key: str
    app_id: str
    secret: str
    engine_model_type: str
    voice_id: str


class ASRMicrosoftVendorParam(BaseModel):
    """
    Microsoft ASR vendor parameter
    
    @since v0.12.0
    """
    key: str
    region: str
    language: str
    phrase_list: List[str]


class ASRDeepgramVendorParam(BaseModel):
    """
    Deepgram ASR vendor parameter
    
    @since v0.12.0
    """
    url: str
    key: str
    model: str
    language: str


# Union type for all ASR vendor parameters
ASRVendorParams = Union[
    ASRFengmingVendorParam,
    ASRAresVendorParam,
    ASRTencentVendorParam,
    ASRMicrosoftVendorParam,
    ASRDeepgramVendorParam,
]


class JoinPropertiesAsrBody(BaseModel):
    """
    Automatic Speech Recognition (ASR) configuration for the agent to join the RTC channel
    
    @since v0.7.0
    """
    language: Optional[str] = Field(
        default="zh-CN",
        description="Language used for interaction: zh-CN (Chinese) or en-US (English)"
    )
    vendor: Optional[ASRVendor] = Field(None, description="ASR vendor")
    params: Optional[ASRVendorParams] = Field(None, description="ASR vendor parameter description")


# ============================================================================
# LLM (Large Language Model) Models
# ============================================================================

class JoinPropertiesCustomLLMBody(BaseModel):
    """
    Custom language model (LLM) configuration for the agent to join the RTC channel
    
    @since v0.7.0
    """
    url: str = Field(..., description="LLM callback URL (required), must be compatible with OpenAI protocol")
    api_key: str = Field(..., description="LLM API key for verification (required)")
    system_messages: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Predefined information attached at the beginning of each LLM call"
    )
    params: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional information transmitted in the LLM message body (e.g., model, max_tokens)"
    )
    max_history: Optional[int] = Field(
        default=32,
        description="Number of short-term memory entries cached in the LLM"
    )
    greeting_message: Optional[str] = Field(
        None,
        description="Agent greeting message sent to the first subscribed user"
    )
    input_modalities: Optional[List[str]] = Field(
        default=["text"],
        description="Input modalities for the LLM: ['text'] or ['text', 'image']"
    )
    output_modalities: Optional[List[str]] = Field(
        default=["text"],
        description="Output modalities for the LLM: ['text'], ['audio'], or ['text', 'audio']"
    )
    failure_message: Optional[str] = Field(
        None,
        description="Failure message returned through TTS when LLM call fails"
    )
    silence_message: Optional[str] = Field(
        None,
        description="Silence prompt message (deprecated since v0.11.0)"
    )
    vendor: Optional[str] = Field(
        default="custom",
        description="LLM provider: custom, aliyun, bytedance, deepseek, tencent"
    )
    style: Optional[str] = Field(
        default="openai",
        description="Request style for chat completion: openai, gemini, anthropic, dify (since v0.11.0)"
    )


# ============================================================================
# MLLM (Multimodal Large Language Model) Models
# ============================================================================

class JoinPropertiesMLLMBody(BaseModel):
    """
    Multi-modal language model (MLLM) configuration
    
    @since v0.12.0
    """
    url: str = Field(..., description="The WebSocket URL for OpenAI Realtime API (Required)")
    api_key: str = Field(..., description="The API key used for authentication (Required)")
    messages: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Array of conversation items used for short-term memory management"
    )
    params: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional MLLM configuration parameters"
    )
    max_history: Optional[int] = Field(
        default=32,
        description="The number of conversation history messages to maintain"
    )
    input_modalities: Optional[List[str]] = Field(
        default=["audio"],
        description="Input modalities for the MLLM: ['audio'] or ['audio', 'text']"
    )
    output_modalities: Optional[List[str]] = Field(
        default=["text", "audio"],
        description="Output format options: ['text', 'audio']"
    )
    greeting_message: Optional[str] = Field(
        None,
        description="Initial message the agent speaks when a user joins the channel"
    )
    vendor: Optional[str] = Field(
        default="openai",
        description="MLLM provider identifier (e.g., 'openai' for OpenAI Realtime API)"
    )
    style: Optional[str] = Field(
        default="openai",
        description="API request style (e.g., 'openai' for OpenAI Realtime API format)"
    )


# ============================================================================
# Advanced Features and Parameters
# ============================================================================

class JoinPropertiesAdvancedFeaturesBody(BaseModel):
    """
    Advanced feature configurations for the agent to join the RTC channel
    
    @since v0.7.0
    """
    enable_aivad: Optional[bool] = Field(
        default=False,
        description="Enable graceful interruption (AIVAD) for natural conversations"
    )
    enable_rtm: Optional[bool] = Field(
        default=False,
        description="Enable Real-time Messaging (RTM) module"
    )
    enable_sal: Optional[bool] = Field(
        default=False,
        description="Enable Speaker Adaptive Learning (SAL)"
    )


class TurnDetectionBody(BaseModel):
    """
    Conversation turn detection settings
    
    @since v0.11.0
    """
    type: Optional[str] = Field(
        default="agora_vad",
        description="Turn detection mechanism: agora_vad, server_vad, semantic_vad (since v0.12.0)"
    )
    interrupt_mode: Optional[str] = Field(
        default="interrupt",
        description="Interrupt mode: interrupt, append, ignore"
    )
    interrupt_duration_ms: Optional[int] = Field(
        default=160,
        description="Time in ms that user's voice must exceed VAD threshold (since v0.12.0)"
    )
    prefix_padding_ms: Optional[int] = Field(
        default=800,
        description="Extra forward padding time in ms before processing speech input (since v0.12.0)"
    )
    silence_duration_ms: Optional[int] = Field(
        default=480,
        description="Duration of audio silence in ms (since v0.12.0)"
    )
    threshold: Optional[float] = Field(
        default=0.5,
        description="Identification sensitivity for voice activity, range (0.0, 1.0) (since v0.12.0)"
    )
    create_response: Optional[bool] = Field(
        default=True,
        description="Auto-generate response when VAD stop event occurs (since v0.12.0)"
    )
    interrupt_response: Optional[bool] = Field(
        default=True,
        description="Auto-interrupt ongoing response when VAD start event occurs (since v0.12.0)"
    )
    eagerness: Optional[str] = Field(
        None,
        description="Model's eagerness to respond: auto, low, high (since v0.12.0)"
    )


class SilenceConfig(BaseModel):
    """
    Silence configuration for the agent
    
    @since v0.11.0
    """
    timeout_ms: Optional[int] = Field(
        None,
        description="Agent maximum silence time in ms, range (0, 60000]"
    )
    action: Optional[str] = Field(
        default="speak",
        description="Action when silence timeout: speak or think"
    )
    content: Optional[str] = Field(
        None,
        description="Content of the silence message"
    )


class FixedParams(BaseModel):
    """
    Fixed parameters
    
    @since v0.11.0
    """
    silence_config: Optional[SilenceConfig] = None
    data_channel: Optional[str] = Field(
        default="datastream",
        description="Agent data transmission channel: rtm or datastream (since v0.12.0)"
    )
    enable_metrics: Optional[bool] = Field(
        default=False,
        description="Whether to receive agent performance data (since v0.12.0)"
    )
    enable_error_message: Optional[bool] = Field(
        default=False,
        description="Whether to receive agent error events (since v0.12.0)"
    )


class Parameters(BaseModel):
    """
    Agent parameters configuration
    
    Note: Contains both extra data and fixed data. Same key in extra data and fixed data will be merged.
    
    @since v0.11.0
    """
    extra_params: Optional[Dict[str, Any]] = Field(
        None,
        description="Extra parameters for flexible key-value pairs"
    )
    fixed_params: Optional[FixedParams] = Field(
        None,
        description="Fixed parameters for type-safe parameters"
    )
    
    def dict(self, **kwargs):
        """Custom dict method to merge extra_params and fixed_params"""
        merged = {}
        
        # Add fixed parameters if present
        if self.fixed_params:
            fixed_dict = self.fixed_params.dict(exclude_none=True)
            merged.update(fixed_dict)
        
        # Add extra parameters if present (will override fixed params with same key)
        if self.extra_params:
            merged.update(self.extra_params)
        
        return merged


# ============================================================================
# Main Join Request Body
# ============================================================================

class JoinPropertiesReqBody(BaseModel):
    """
    Request body for calling the Conversational AI engine Join API
    
    @since v0.7.0
    """
    token: str = Field(..., description="Token used to join the RTC channel (dynamic key for authentication)")
    channel: str = Field(..., description="RTC channel name the agent joins (required)")
    agent_rtc_uid: str = Field(..., description="User ID of the agent in the RTC channel (required)")
    remote_rtc_uids: List[str] = Field(
        ...,
        description="List of user IDs the agent subscribes to. Use ['*'] to subscribe to all users"
    )
    enable_string_uid: Optional[bool] = Field(
        default=False,
        description="Whether to enable String UID"
    )
    idle_timeout: Optional[int] = Field(
        default=180,
        description="Maximum idle time of the RTC channel in seconds"
    )
    silence_timeout: Optional[int] = Field(
        None,
        description="Maximum silence time of the agent in seconds (deprecated since v0.11.0)"
    )
    agent_rtm_uid: Optional[str] = Field(
        None,
        description="Agent user ID in the RTM channel (deprecated since v0.11.0)"
    )
    advanced_features: Optional[JoinPropertiesAdvancedFeaturesBody] = Field(
        None,
        description="Advanced feature configurations"
    )
    llm: Optional[JoinPropertiesCustomLLMBody] = Field(
        None,
        description="Custom language model (LLM) configuration (required)"
    )
    mllm: Optional[JoinPropertiesMLLMBody] = Field(
        None,
        description="Multimodal Large Language Model (MLLM) configuration (since v0.12.0)"
    )
    tts: Optional[JoinPropertiesTTSBody] = Field(
        None,
        description="Text-to-Speech (TTS) module configuration (required)"
    )
    asr: Optional[JoinPropertiesAsrBody] = Field(
        None,
        description="Automatic Speech Recognition (ASR) configuration"
    )
    turn_detection: Optional[TurnDetectionBody] = Field(
        None,
        description="Conversation turn detection settings"
    )
    parameters: Optional[Parameters] = Field(
        None,
        description="Agent parameters configuration"
    )
    
    class Config:
        use_enum_values = True  # Use enum values instead of enum objects in serialization
    
    def dict(self, **kwargs):
        """Custom dict method to handle Parameters serialization"""
        # Get base dict
        result = super().dict(**kwargs)
        
        # Handle parameters field specially
        if self.parameters is not None:
            result['parameters'] = self.parameters.dict()
        
        return result

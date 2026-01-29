"""
Agora Conversational AI API Request Models

Corresponds to Go version: agora-rest-client-go/services/convoai/req/
"""

from .join import (
    # TTS Models
    TTSVendor,
    TTSMinimaxVendorParams,
    TTSMinimaxVendorVoiceSettingParam,
    TTSMinimaxVendorAudioSettingParam,
    TTSTencentVendorParams,
    TTSBytedanceVendorParams,
    TTSMicrosoftVendorParams,
    TTSElevenLabsVendorParams,
    TTSCartesiaVendorParams,
    TTSOpenAIVendorParams,
    JoinPropertiesTTSBody,
    # ASR Models
    ASRVendor,
    ASRFengmingVendorParam,
    ASRAresVendorParam,
    ASRTencentVendorParam,
    ASRMicrosoftVendorParam,
    ASRDeepgramVendorParam,
    JoinPropertiesAsrBody,
    # LLM Models
    JoinPropertiesCustomLLMBody,
    # MLLM Models
    JoinPropertiesMLLMBody,
    # Advanced Features
    JoinPropertiesAdvancedFeaturesBody,
    TurnDetectionBody,
    SilenceConfig,
    FixedParams,
    Parameters,
    # Main Request Body
    JoinPropertiesReqBody,
)

__all__ = [
    # TTS
    "TTSVendor",
    "TTSMinimaxVendorParams",
    "TTSMinimaxVendorVoiceSettingParam",
    "TTSMinimaxVendorAudioSettingParam",
    "TTSTencentVendorParams",
    "TTSBytedanceVendorParams",
    "TTSMicrosoftVendorParams",
    "TTSElevenLabsVendorParams",
    "TTSCartesiaVendorParams",
    "TTSOpenAIVendorParams",
    "JoinPropertiesTTSBody",
    # ASR
    "ASRVendor",
    "ASRFengmingVendorParam",
    "ASRAresVendorParam",
    "ASRTencentVendorParam",
    "ASRMicrosoftVendorParam",
    "ASRDeepgramVendorParam",
    "JoinPropertiesAsrBody",
    # LLM
    "JoinPropertiesCustomLLMBody",
    # MLLM
    "JoinPropertiesMLLMBody",
    # Advanced Features
    "JoinPropertiesAdvancedFeaturesBody",
    "TurnDetectionBody",
    "SilenceConfig",
    "FixedParams",
    "Parameters",
    # Main Request Body
    "JoinPropertiesReqBody",
]

"""
Property Builder

Builds agent properties for Agora Conversational AI join requests.
Supports Deepgram (ASR), OpenAI (LLM), ElevenLabs (TTS).
"""
from typing import Dict, Any

from ..req import (
    JoinPropertiesReqBody,
    JoinPropertiesAdvancedFeaturesBody,
    JoinPropertiesCustomLLMBody,
    JoinPropertiesTTSBody,
    JoinPropertiesAsrBody,
    TTSElevenLabsVendorParams,
    ASRDeepgramVendorParam,
    TurnDetectionBody,
    Parameters,
    FixedParams,
)


class PropertyBuilder:
    """Builds agent properties for join requests"""
    
    @staticmethod
    def build_join_properties(
        channel: str,
        agent_uid: str,
        user_uid: str,
        token: str,
        asr_config: Dict[str, Any],
        llm_config: Dict[str, Any],
        tts_config: Dict[str, Any]
    ) -> JoinPropertiesReqBody:
        """Build complete join properties request body"""
        return JoinPropertiesReqBody(
            token=token,
            channel=channel,
            agent_rtc_uid=agent_uid,
            remote_rtc_uids=[user_uid],
            enable_string_uid=False,
            idle_timeout=120,
            silence_timeout=30,
            advanced_features=PropertyBuilder._build_advanced_features(),
            llm=PropertyBuilder._build_llm(llm_config),
            tts=PropertyBuilder._build_tts(tts_config),
            asr=PropertyBuilder._build_asr(asr_config),
            turn_detection=PropertyBuilder._build_turn_detection(),
            parameters=PropertyBuilder._build_parameters(),
        )
    
    @staticmethod
    def _build_llm(llm_config: Dict[str, Any]) -> JoinPropertiesCustomLLMBody:
        """Build LLM configuration"""
        system_msg = llm_config.get("system_message", "You are a helpful assistant.")
        greeting_msg = llm_config.get("greeting", "Hello, how can I help you?")
        
        return JoinPropertiesCustomLLMBody(
            url=llm_config.get("url"),
            api_key=llm_config.get("api_key"),
            system_messages=[{"role": "system", "content": system_msg}],
            params={
                "model": llm_config.get("model"),
                "max_tokens": llm_config.get("max_tokens", 1024),
            },
            max_history=llm_config.get("max_history", 64),
            greeting_message=greeting_msg,
            input_modalities=["text"],
            output_modalities=["text"],
        )
    
    @staticmethod
    def _build_tts(tts_config: Dict[str, Any]) -> JoinPropertiesTTSBody:
        """Build TTS configuration"""
        vendor = tts_config.get("vendor")
        if vendor != "elevenlabs":
            raise ValueError(f"Unsupported TTS vendor: {vendor}")
        
        params = TTSElevenLabsVendorParams(
            key=tts_config.get("api_key"),
            model_id=tts_config.get("model_id", "eleven_multilingual_v2"),
            voice_id=tts_config.get("voice_id", "pNInz6obpgDQGcFmaJgB"),
        )
        return JoinPropertiesTTSBody(vendor="elevenlabs", params=params)
    
    @staticmethod
    def _build_asr(asr_config: Dict[str, Any]) -> JoinPropertiesAsrBody:
        """Build ASR configuration"""
        vendor = asr_config.get("vendor")
        if vendor != "deepgram":
            raise ValueError(f"Unsupported ASR vendor: {vendor}")
        
        params = ASRDeepgramVendorParam(
            url=asr_config.get("url", "wss://api.deepgram.com/v1/listen"),
            key=asr_config.get("api_key"),
            model=asr_config.get("model", "nova-2"),
            language=asr_config.get("language", "en-US"),
        )
        return JoinPropertiesAsrBody(vendor="deepgram", params=params)
    
    @staticmethod
    def _build_turn_detection() -> TurnDetectionBody:
        """Build turn detection configuration"""
        return TurnDetectionBody(
            interrupt_duration_ms=160,
            prefix_padding_ms=300,
            silence_duration_ms=480,
            threshold=0.5,
        )
    
    @staticmethod
    def _build_advanced_features() -> JoinPropertiesAdvancedFeaturesBody:
        """Build advanced features configuration"""
        return JoinPropertiesAdvancedFeaturesBody(
            enable_aivad=True,
            enable_rtm=True,
            enable_sal=True,
        )
    
    @staticmethod
    def _build_parameters() -> Parameters:
        """Build agent parameters"""
        return Parameters(
            fixed_params=FixedParams(
                data_channel="rtm",
                enable_metrics=True,
                enable_error_message=True,
            )
        )

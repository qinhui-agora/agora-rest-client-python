"""
Property Builder

Builds agent properties for Agora Conversational AI join requests.
Supports all built-in vendors from Agora REST API.

Built-in ASR vendors: deepgram, fengming, tencent, microsoft, ares
Built-in TTS vendors: elevenlabs, minimax, tencent, bytedance, microsoft, cartesia, openai
Built-in LLM vendors: custom (OpenAI-compatible)

For custom vendors not listed above, use the 'params' field to pass vendor-specific parameters.
"""
from typing import Dict, Any

from ..req import (
    JoinPropertiesReqBody,
    JoinPropertiesAdvancedFeaturesBody,
    JoinPropertiesCustomLLMBody,
    JoinPropertiesTTSBody,
    JoinPropertiesAsrBody,
    # TTS vendor params
    TTSElevenLabsVendorParams,
    TTSMinimaxVendorParams,
    TTSTencentVendorParams,
    TTSBytedanceVendorParams,
    TTSMicrosoftVendorParams,
    TTSCartesiaVendorParams,
    TTSOpenAIVendorParams,
    # ASR vendor params
    ASRDeepgramVendorParam,
    ASRFengmingVendorParam,
    ASRAresVendorParam,
    ASRTencentVendorParam,
    ASRMicrosoftVendorParam,
    # Other
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
        """
        Build LLM configuration
        
        Supports OpenAI and compatible APIs by default.
        For custom LLM providers, you can pass the complete configuration.
        
        Args:
            llm_config: LLM configuration dict with either:
                - Standard fields: api_key, url, model, max_tokens, etc.
                - Or complete JoinPropertiesCustomLLMBody fields for custom providers
        """
        system_msg = llm_config.get("system_message", "You are a helpful assistant.")
        greeting_msg = llm_config.get("greeting", "Hello, how can I help you?")
        
        return JoinPropertiesCustomLLMBody(
            url=llm_config.get("url"),
            api_key=llm_config.get("api_key"),
            system_messages=llm_config.get("system_messages", [{"role": "system", "content": system_msg}]),
            params=llm_config.get("params", {
                "model": llm_config.get("model"),
                "max_tokens": llm_config.get("max_tokens", 1024),
            }),
            max_history=llm_config.get("max_history", 64),
            greeting_message=llm_config.get("greeting_message", greeting_msg),
            input_modalities=llm_config.get("input_modalities", ["text"]),
            output_modalities=llm_config.get("output_modalities", ["text"]),
        )
    
    @staticmethod
    def _build_tts(tts_config: Dict[str, Any]) -> JoinPropertiesTTSBody:
        """
        Build TTS configuration
        
        Supports built-in vendors: elevenlabs, minimax, tencent, bytedance, microsoft, cartesia, openai
        For other TTS providers, pass 'params' directly.
        
        Args:
            tts_config: TTS configuration with either:
                - Config object with to_pydantic() method (ElevenLabsTTSConfig, etc.)
                - Dict with built-in vendor fields (vendor, api_key, etc.)
                - Dict with custom vendor: vendor, params
        
        Examples:
            # Using config object (recommended)
            ElevenLabsTTSConfig(api_key="xxx")
            
            # Using dict
            {"vendor": "elevenlabs", "api_key": "xxx", "voice_id": "yyy"}
            
            # Custom vendor
            {"vendor": "custom", "params": {"api_key": "xxx", "custom_param": "value"}}
        """
        # If tts_config has to_pydantic() method, use it
        if hasattr(tts_config, 'to_pydantic') and callable(tts_config.to_pydantic):
            pydantic_model = tts_config.to_pydantic()
            # Determine vendor from class name
            class_name = tts_config.__class__.__name__
            vendor_map = {
                'ElevenLabsTTSConfig': 'elevenlabs',
                'MinimaxTTSConfig': 'minimax',
                'TencentTTSConfig': 'tencent',
                'BytedanceTTSConfig': 'bytedance',
                'MicrosoftTTSConfig': 'microsoft',
                'CartesiaTTSConfig': 'cartesia',
                'OpenAITTSConfig': 'openai',
            }
            vendor = vendor_map.get(class_name, 'custom')
            return JoinPropertiesTTSBody(vendor=vendor, params=pydantic_model)
        
        vendor = tts_config.get("vendor")
        
        # If user provides params directly, use them (for custom vendors)
        if "params" in tts_config:
            return JoinPropertiesTTSBody(vendor=vendor, params=tts_config["params"])
        
        # Built-in vendor: ElevenLabs
        if vendor == "elevenlabs":
            params = TTSElevenLabsVendorParams(
                key=tts_config.get("api_key") or tts_config.get("key"),
                model_id=tts_config.get("model_id", "eleven_multilingual_v2"),
                voice_id=tts_config.get("voice_id", "pNInz6obpgDQGcFmaJgB"),
                sample_rate=tts_config.get("sample_rate", 24000),
                stability=tts_config.get("stability"),
                similarity_boost=tts_config.get("similarity_boost"),
                style=tts_config.get("style"),
                use_speaker_boost=tts_config.get("use_speaker_boost"),
            )
            return JoinPropertiesTTSBody(vendor="elevenlabs", params=params)
        
        # Built-in vendor: Minimax
        elif vendor == "minimax":
            from ..req import TTSMinimaxVendorVoiceSettingParam, TTSMinimaxVendorAudioSettingParam
            
            voice_setting = None
            if any(k in tts_config for k in ["voice_id", "speed", "vol", "pitch", "emotion"]):
                voice_setting = TTSMinimaxVendorVoiceSettingParam(
                    voice_id=tts_config.get("voice_id", ""),
                    speed=tts_config.get("speed", 1.0),
                    vol=tts_config.get("vol", 1.0),
                    pitch=tts_config.get("pitch", 0),
                    emotion=tts_config.get("emotion", "neutral"),
                    latex_render=tts_config.get("latex_render"),
                    english_normalization=tts_config.get("english_normalization"),
                )
            
            audio_setting = None
            if "sample_rate" in tts_config:
                audio_setting = TTSMinimaxVendorAudioSettingParam(
                    sample_rate=tts_config.get("sample_rate", 24000)
                )
            
            params = TTSMinimaxVendorParams(
                group_id=tts_config.get("group_id"),
                key=tts_config.get("key"),
                model=tts_config.get("model"),
                voice_setting=voice_setting,
                audio_setting=audio_setting,
                url=tts_config.get("url"),
            )
            return JoinPropertiesTTSBody(vendor="minimax", params=params)
        
        # Built-in vendor: Tencent
        elif vendor == "tencent":
            params = TTSTencentVendorParams(
                app_id=tts_config.get("app_id"),
                secret_id=tts_config.get("secret_id"),
                secret_key=tts_config.get("secret_key"),
                voice_type=tts_config.get("voice_type", 0),
                volume=tts_config.get("volume", 0),
                speed=tts_config.get("speed", 0),
                emotion_category=tts_config.get("emotion_category", ""),
                emotion_intensity=tts_config.get("emotion_intensity", 0),
            )
            return JoinPropertiesTTSBody(vendor="tencent", params=params)
        
        # Built-in vendor: Bytedance
        elif vendor == "bytedance":
            params = TTSBytedanceVendorParams(
                token=tts_config.get("token"),
                app_id=tts_config.get("app_id"),
                cluster=tts_config.get("cluster"),
                voice_type=tts_config.get("voice_type"),
                speed_ratio=tts_config.get("speed_ratio", 1.0),
                volume_ratio=tts_config.get("volume_ratio", 1.0),
                pitch_ratio=tts_config.get("pitch_ratio", 1.0),
                emotion=tts_config.get("emotion", ""),
            )
            return JoinPropertiesTTSBody(vendor="bytedance", params=params)
        
        # Built-in vendor: Microsoft
        elif vendor == "microsoft":
            params = TTSMicrosoftVendorParams(
                key=tts_config.get("key"),
                region=tts_config.get("region", "eastus"),
                voice_name=tts_config.get("voice_name", "en-US-JennyNeural"),
                speed=tts_config.get("speed", 1.0),
                volume=tts_config.get("volume", 100.0),
                sample_rate=tts_config.get("sample_rate", 24000),
            )
            return JoinPropertiesTTSBody(vendor="microsoft", params=params)
        
        # Built-in vendor: Cartesia
        elif vendor == "cartesia":
            from ..req import TTSCartesiaVendorVoice
            
            voice = None
            if "voice_mode" in tts_config and "voice_id" in tts_config:
                voice = TTSCartesiaVendorVoice(
                    mode=tts_config.get("voice_mode", "id"),
                    id=tts_config.get("voice_id", ""),
                )
            
            params = TTSCartesiaVendorParams(
                api_key=tts_config.get("api_key"),
                model_id=tts_config.get("model_id"),
                voice=voice,
            )
            return JoinPropertiesTTSBody(vendor="cartesia", params=params)
        
        # Built-in vendor: OpenAI
        elif vendor == "openai":
            params = TTSOpenAIVendorParams(
                api_key=tts_config.get("api_key"),
                model=tts_config.get("model", "tts-1"),
                voice=tts_config.get("voice", "alloy"),
                instructions=tts_config.get("instructions", ""),
                speed=tts_config.get("speed", 1.0),
            )
            return JoinPropertiesTTSBody(vendor="openai", params=params)
        
        # Unsupported vendor without params
        raise ValueError(
            f"Unsupported TTS vendor: '{vendor}'. "
            f"Supported built-in vendors: elevenlabs, minimax, tencent, bytedance, microsoft, cartesia, openai. "
            f"For other vendors, please provide 'params' field with vendor-specific parameters."
        )
    
    @staticmethod
    def _build_asr(asr_config: Dict[str, Any]) -> JoinPropertiesAsrBody:
        """
        Build ASR configuration
        
        Supports built-in vendors: deepgram, fengming, tencent, microsoft, ares
        For other ASR providers, pass 'params' directly.
        
        Args:
            asr_config: ASR configuration with either:
                - Config object with to_pydantic() method (DeepgramASRConfig, etc.)
                - Dict with built-in vendor fields (vendor, api_key, etc.)
                - Dict with custom vendor: vendor, params
        
        Examples:
            # Using config object (recommended)
            DeepgramASRConfig(api_key="xxx")
            
            # Using dict
            {"vendor": "deepgram", "api_key": "xxx", "model": "nova-2", "language": "en-US"}
            
            # Custom vendor
            {"vendor": "custom", "params": {"api_key": "xxx", "custom_param": "value"}}
        """
        # If asr_config has to_pydantic() method, use it
        if hasattr(asr_config, 'to_pydantic') and callable(asr_config.to_pydantic):
            pydantic_model = asr_config.to_pydantic()
            # Determine vendor from class name
            class_name = asr_config.__class__.__name__
            vendor_map = {
                'DeepgramASRConfig': 'deepgram',
                'FengmingASRConfig': 'fengming',
                'TencentASRConfig': 'tencent',
                'MicrosoftASRConfig': 'microsoft',
                'AresASRConfig': 'ares',
            }
            vendor = vendor_map.get(class_name, 'custom')
            return JoinPropertiesAsrBody(vendor=vendor, params=pydantic_model)
        
        vendor = asr_config.get("vendor")
        
        # If user provides params directly, use them (for custom vendors)
        if "params" in asr_config:
            return JoinPropertiesAsrBody(vendor=vendor, params=asr_config["params"])
        
        # Built-in vendor: Deepgram
        if vendor == "deepgram":
            params = ASRDeepgramVendorParam(
                url=asr_config.get("url", "wss://api.deepgram.com/v1/listen"),
                key=asr_config.get("api_key") or asr_config.get("key"),
                model=asr_config.get("model", "nova-2"),
                language=asr_config.get("language", "en-US"),
            )
            return JoinPropertiesAsrBody(vendor="deepgram", params=params)
        
        # Built-in vendor: Fengming
        elif vendor == "fengming":
            params = ASRFengmingVendorParam()
            return JoinPropertiesAsrBody(vendor="fengming", params=params)
        
        # Built-in vendor: Tencent
        elif vendor == "tencent":
            params = ASRTencentVendorParam(
                key=asr_config.get("key"),
                app_id=asr_config.get("app_id"),
                secret=asr_config.get("secret"),
                engine_model_type=asr_config.get("engine_model_type", "16k_zh"),
                voice_id=asr_config.get("voice_id"),
            )
            return JoinPropertiesAsrBody(vendor="tencent", params=params)
        
        # Built-in vendor: Microsoft
        elif vendor == "microsoft":
            params = ASRMicrosoftVendorParam(
                key=asr_config.get("key"),
                region=asr_config.get("region", "eastus"),
                language=asr_config.get("language", "en-US"),
                phrase_list=asr_config.get("phrase_list", []),
            )
            return JoinPropertiesAsrBody(vendor="microsoft", params=params)
        
        # Built-in vendor: Ares
        elif vendor == "ares":
            params = ASRAresVendorParam()
            return JoinPropertiesAsrBody(vendor="ares", params=params)
        
        # Unsupported vendor without params
        raise ValueError(
            f"Unsupported ASR vendor: '{vendor}'. "
            f"Supported built-in vendors: deepgram, fengming, tencent, microsoft, ares. "
            f"For other vendors, please provide 'params' field with vendor-specific parameters."
        )
    
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

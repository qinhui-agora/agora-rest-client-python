"""
Unit tests for configuration components
"""
import pytest
from agora_rest.agent import (
    DeepgramASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig,
    BaseASRConfig,
    BaseLLMConfig,
    BaseTTSConfig,
)


class TestDeepgramASRConfig:
    """Test DeepgramASRConfig"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = DeepgramASRConfig(api_key="test_key")
        
        assert config.vendor == "deepgram"
        assert config.api_key == "test_key"
        assert config.url == "wss://api.deepgram.com/v1/listen"
        assert config.model == "nova-2"
        assert config.language == "en-US"
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = DeepgramASRConfig(
            api_key="test_key",
            model="nova-3",
            language="zh-CN"
        )
        
        assert config.model == "nova-3"
        assert config.language == "zh-CN"
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        config = DeepgramASRConfig(api_key="test_key")
        result = config.to_dict()
        
        assert isinstance(result, dict)
        assert result["vendor"] == "deepgram"
        assert result["api_key"] == "test_key"
        assert "url" in result
        assert "model" in result


class TestOpenAILLMConfig:
    """Test OpenAILLMConfig"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = OpenAILLMConfig(api_key="test_key")
        
        assert config.api_key == "test_key"
        assert config.url == "https://api.openai.com/v1"
        assert config.model == "gpt-4"
        assert config.max_tokens == 1024
        assert config.system_message == "You are a helpful assistant."
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = OpenAILLMConfig(
            api_key="test_key",
            model="gpt-4o",
            system_message="Custom message",
            max_tokens=2048
        )
        
        assert config.model == "gpt-4o"
        assert config.system_message == "Custom message"
        assert config.max_tokens == 2048
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        config = OpenAILLMConfig(api_key="test_key")
        result = config.to_dict()
        
        assert isinstance(result, dict)
        assert result["api_key"] == "test_key"
        assert result["model"] == "gpt-4"


class TestElevenLabsTTSConfig:
    """Test ElevenLabsTTSConfig"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = ElevenLabsTTSConfig(api_key="test_key")
        
        assert config.vendor == "elevenlabs"
        assert config.api_key == "test_key"
        assert config.model_id == "eleven_multilingual_v2"
        assert config.voice_id == "pNInz6obpgDQGcFmaJgB"
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = ElevenLabsTTSConfig(
            api_key="test_key",
            voice_id="custom_voice_id"
        )
        
        assert config.voice_id == "custom_voice_id"
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        config = ElevenLabsTTSConfig(api_key="test_key")
        result = config.to_dict()
        
        assert isinstance(result, dict)
        assert result["vendor"] == "elevenlabs"
        assert result["api_key"] == "test_key"


class TestCustomConfigs:
    """Test custom configuration classes"""
    
    def test_custom_asr_config(self):
        """Test creating custom ASR configuration"""
        from dataclasses import dataclass
        
        @dataclass
        class CustomASRConfig(BaseASRConfig):
            vendor: str = "custom_vendor"
            api_key: str = ""
            custom_param: str = "value"
        
        config = CustomASRConfig(api_key="test_key", custom_param="custom_value")
        result = config.to_dict()
        
        assert result["vendor"] == "custom_vendor"
        assert result["api_key"] == "test_key"
        assert result["custom_param"] == "custom_value"

"""
Unit tests for configuration components
"""
import pytest
from agora_rest.agent import (
    DeepgramASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig,
    MicrosoftASRConfig,
    MicrosoftTTSConfig,
    OpenAITTSConfig,
)


class TestDeepgramASRConfig:
    """Test DeepgramASRConfig (dataclass wrapper)"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = DeepgramASRConfig(api_key="test_key")
        
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
    
    def test_to_pydantic(self):
        """Test conversion to Pydantic model"""
        config = DeepgramASRConfig(api_key="test_key")
        pydantic_model = config.to_pydantic()
        
        assert pydantic_model.key == "test_key"
        assert pydantic_model.url == "wss://api.deepgram.com/v1/listen"
        assert pydantic_model.model == "nova-2"


class TestMicrosoftASRConfig:
    """Test MicrosoftASRConfig (dataclass wrapper)"""
    
    def test_creation(self):
        """Test Microsoft ASR configuration"""
        config = MicrosoftASRConfig(key="test_key")
        
        assert config.key == "test_key"
        assert config.region == "eastus"
        assert config.language == "en-US"
        assert config.phrase_list == []
    
    def test_to_pydantic(self):
        """Test conversion to Pydantic model"""
        config = MicrosoftASRConfig(
            key="test_key",
            region="westus",
            language="zh-CN"
        )
        pydantic_model = config.to_pydantic()
        
        assert pydantic_model.key == "test_key"
        assert pydantic_model.region == "westus"
        assert pydantic_model.language == "zh-CN"


class TestOpenAILLMConfig:
    """Test OpenAILLMConfig (dataclass)"""
    
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
    """Test ElevenLabsTTSConfig (dataclass wrapper)"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = ElevenLabsTTSConfig(api_key="test_key")
        
        assert config.api_key == "test_key"
        assert config.model_id == "eleven_multilingual_v2"
        assert config.voice_id == "pNInz6obpgDQGcFmaJgB"
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = ElevenLabsTTSConfig(
            api_key="test_key",
            voice_id="custom_voice_id",
            stability=0.5,
            similarity_boost=0.8
        )
        
        assert config.voice_id == "custom_voice_id"
        assert config.stability == 0.5
        assert config.similarity_boost == 0.8
    
    def test_to_pydantic(self):
        """Test conversion to Pydantic model"""
        config = ElevenLabsTTSConfig(api_key="test_key")
        pydantic_model = config.to_pydantic()
        
        assert pydantic_model.key == "test_key"
        assert pydantic_model.model_id == "eleven_multilingual_v2"
        assert pydantic_model.voice_id == "pNInz6obpgDQGcFmaJgB"


class TestMicrosoftTTSConfig:
    """Test MicrosoftTTSConfig (dataclass wrapper)"""
    
    def test_creation(self):
        """Test Microsoft TTS configuration"""
        config = MicrosoftTTSConfig(key="test_key")
        
        assert config.key == "test_key"
        assert config.region == "eastus"
        assert config.voice_name == "en-US-JennyNeural"
    
    def test_to_pydantic(self):
        """Test conversion to Pydantic model"""
        config = MicrosoftTTSConfig(
            key="test_key",
            region="westus",
            voice_name="zh-CN-XiaoxiaoNeural"
        )
        pydantic_model = config.to_pydantic()
        
        assert pydantic_model.key == "test_key"
        assert pydantic_model.region == "westus"
        assert pydantic_model.voice_name == "zh-CN-XiaoxiaoNeural"


class TestOpenAITTSConfig:
    """Test OpenAITTSConfig (dataclass wrapper)"""
    
    def test_creation(self):
        """Test OpenAI TTS configuration"""
        config = OpenAITTSConfig(api_key="test_key")
        
        assert config.api_key == "test_key"
        assert config.model == "tts-1"
        assert config.voice == "alloy"
    
    def test_to_pydantic(self):
        """Test conversion to Pydantic model"""
        config = OpenAITTSConfig(
            api_key="test_key",
            model="tts-1-hd",
            voice="nova"
        )
        pydantic_model = config.to_pydantic()
        
        assert pydantic_model.api_key == "test_key"
        assert pydantic_model.model == "tts-1-hd"
        assert pydantic_model.voice == "nova"

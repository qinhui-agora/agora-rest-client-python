"""
Integration tests for AgentClient

These tests make real API calls and require valid credentials.
Set environment variables before running:
- APP_ID
- APP_CERTIFICATE
- API_KEY
- API_SECRET
- LLM_API_KEY
- ASR_DEEPGRAM_API_KEY (optional)
- TTS_ELEVENLABS_API_KEY (optional)

Run with: pytest tests/integration/ -v
Skip with: pytest tests/ --ignore=tests/integration/
"""
import os
import time
import pytest
from agora_rest import AgentClient
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig


# Skip all tests if credentials are not available
pytestmark = pytest.mark.skipif(
    not all([
        os.getenv("APP_ID"),
        os.getenv("APP_CERTIFICATE"),
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
        os.getenv("LLM_API_KEY"),
    ]),
    reason="Integration tests require real API credentials"
)


@pytest.fixture
def client():
    """Create AgentClient with real credentials"""
    return AgentClient(
        app_id=os.getenv("APP_ID"),
        app_certificate=os.getenv("APP_CERTIFICATE"),
        customer_id=os.getenv("API_KEY"),
        customer_secret=os.getenv("API_SECRET")
    )


@pytest.fixture
def config_data(client):
    """Generate connection configuration"""
    return client.generate_config()


@pytest.fixture
def asr_config():
    """Create ASR configuration"""
    api_key = os.getenv("ASR_DEEPGRAM_API_KEY")
    if not api_key:
        pytest.skip("ASR_DEEPGRAM_API_KEY not set")
    return DeepgramASRConfig(api_key=api_key)


@pytest.fixture
def llm_config():
    """Create LLM configuration"""
    return OpenAILLMConfig(api_key=os.getenv("LLM_API_KEY"))


@pytest.fixture
def tts_config():
    """Create TTS configuration"""
    api_key = os.getenv("TTS_ELEVENLABS_API_KEY")
    if not api_key:
        pytest.skip("TTS_ELEVENLABS_API_KEY not set")
    return ElevenLabsTTSConfig(api_key=api_key)


class TestAgentIntegration:
    """Integration tests for agent lifecycle"""
    
    def test_generate_config(self, client):
        """Test generating connection configuration"""
        config = client.generate_config()
        
        assert "app_id" in config
        assert "token" in config
        assert "uid" in config
        assert "channel_name" in config
        assert "agent_uid" in config
        assert len(config["token"]) > 0
        assert config["channel_name"].startswith("channel_")
    
    def test_start_and_stop_agent(self, client, config_data, asr_config, llm_config, tts_config):
        """Test complete agent lifecycle: start and stop"""
        # Start agent
        result = client.start_agent(
            channel_name=config_data['channel_name'],
            agent_uid=config_data['agent_uid'],
            user_uid=config_data['uid'],
            asr_config=asr_config,
            llm_config=llm_config,
            tts_config=tts_config
        )
        
        # Verify start result
        assert "agent_id" in result
        assert result["channel_name"] == config_data['channel_name']
        assert result["status"] == "started"
        
        agent_id = result["agent_id"]
        print(f"\n✓ Agent started: {agent_id}")
        
        # Wait a bit to ensure agent is running
        time.sleep(2)
        
        # Stop agent
        try:
            client.stop_agent(agent_id)
            print(f"✓ Agent stopped: {agent_id}")
        except Exception as e:
            pytest.fail(f"Failed to stop agent: {e}")
    
    def test_start_agent_with_custom_llm_config(self, client, config_data, asr_config, tts_config):
        """Test starting agent with customized LLM configuration"""
        # Custom LLM config
        llm = OpenAILLMConfig(
            api_key=os.getenv("LLM_API_KEY"),
            model="gpt-4",
            system_message="You are a friendly AI assistant.",
            greeting="Hello! How can I assist you today?",
            max_tokens=512
        )
        
        # Start agent
        result = client.start_agent(
            channel_name=config_data['channel_name'],
            agent_uid=config_data['agent_uid'],
            user_uid=config_data['uid'],
            asr_config=asr_config,
            llm_config=llm,
            tts_config=tts_config
        )
        
        agent_id = result["agent_id"]
        print(f"\n✓ Agent started with custom config: {agent_id}")
        
        # Cleanup
        time.sleep(1)
        client.stop_agent(agent_id)
        print(f"✓ Agent stopped: {agent_id}")

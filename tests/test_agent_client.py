"""
Unit tests for AgentClient

These tests use mocks to avoid making real API calls.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from agora_rest import AgentClient
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig


class TestAgentClient:
    """Test AgentClient class"""
    
    def test_init_with_all_params(self):
        """Test initialization with all required parameters"""
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        assert client.app_id == "test_app_id"
        assert client.app_certificate == "test_cert"
        assert client.customer_id == "test_customer_id"
        assert client.customer_secret == "test_secret"
    
    def test_init_missing_params(self):
        """Test initialization fails with missing parameters"""
        with pytest.raises(ValueError, match="All parameters are required"):
            AgentClient(
                app_id="test_app_id",
                app_certificate="test_cert",
                customer_id="test_customer_id",
                customer_secret=""  # Missing
            )
    
    def test_generate_config(self):
        """Test generate_config creates valid configuration"""
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        config = client.generate_config()
        
        assert "app_id" in config
        assert "token" in config
        assert "uid" in config
        assert "channel_name" in config
        assert "agent_uid" in config
        assert config["app_id"] == "test_app_id"
        assert config["channel_name"].startswith("channel_")
    
    @patch('agora_rest.agent.client.ConvoAIClient')
    def test_start_agent_success(self, mock_convo_client):
        """Test start_agent with successful response"""
        # Setup mock
        mock_response = Mock()
        mock_response.success_resp = Mock(agent_id="test_agent_123")
        mock_response.err_response = None
        
        mock_client_instance = Mock()
        mock_client_instance.join.return_value = mock_response
        mock_convo_client.return_value = mock_client_instance
        
        # Create client
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        # Configure components
        asr = DeepgramASRConfig(api_key="test_asr_key")
        llm = OpenAILLMConfig(api_key="test_llm_key")
        tts = ElevenLabsTTSConfig(api_key="test_tts_key")
        
        # Start agent
        result = client.start_agent(
            channel_name="test_channel",
            agent_uid="123456",
            user_uid="789012",
            asr_config=asr,
            llm_config=llm,
            tts_config=tts
        )
        
        # Assertions
        assert result["agent_id"] == "test_agent_123"
        assert result["channel_name"] == "test_channel"
        assert result["status"] == "started"
        mock_client_instance.join.assert_called_once()
    
    @patch('agora_rest.agent.client.ConvoAIClient')
    def test_start_agent_failure(self, mock_convo_client):
        """Test start_agent with error response"""
        # Setup mock
        mock_response = Mock()
        mock_response.success_resp = None
        mock_response.err_response = Mock(reason="InvalidToken", detail="Token expired")
        
        mock_client_instance = Mock()
        mock_client_instance.join.return_value = mock_response
        mock_convo_client.return_value = mock_client_instance
        
        # Create client
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        # Configure components
        asr = DeepgramASRConfig(api_key="test_asr_key")
        llm = OpenAILLMConfig(api_key="test_llm_key")
        tts = ElevenLabsTTSConfig(api_key="test_tts_key")
        
        # Start agent should raise error
        with pytest.raises(RuntimeError, match="Failed to start agent"):
            client.start_agent(
                channel_name="test_channel",
                agent_uid="123456",
                user_uid="789012",
                asr_config=asr,
                llm_config=llm,
                tts_config=tts
            )
    
    @patch('agora_rest.agent.client.ConvoAIClient')
    def test_start_agent_with_dict_config(self, mock_convo_client):
        """Test start_agent accepts dictionary configurations"""
        # Setup mock
        mock_response = Mock()
        mock_response.success_resp = Mock(agent_id="test_agent_123")
        mock_response.err_response = None
        
        mock_client_instance = Mock()
        mock_client_instance.join.return_value = mock_response
        mock_convo_client.return_value = mock_client_instance
        
        # Create client
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        # Use dictionary configurations
        result = client.start_agent(
            channel_name="test_channel",
            agent_uid="123456",
            user_uid="789012",
            asr_config={"vendor": "deepgram", "api_key": "test_key"},
            llm_config={"api_key": "test_key", "model": "gpt-4"},
            tts_config={"vendor": "elevenlabs", "api_key": "test_key"}
        )
        
        assert result["agent_id"] == "test_agent_123"
    
    @patch('agora_rest.agent.client.ConvoAIClient')
    def test_stop_agent(self, mock_convo_client):
        """Test stop_agent calls leave API"""
        mock_client_instance = Mock()
        mock_convo_client.return_value = mock_client_instance
        
        client = AgentClient(
            app_id="test_app_id",
            app_certificate="test_cert",
            customer_id="test_customer_id",
            customer_secret="test_secret"
        )
        
        client.stop_agent("test_agent_123")
        
        mock_client_instance.leave.assert_called_once_with("test_agent_123")

"""
Agent Client

Handles business logic and API calls for Agora Conversational AI Agents.
"""
import json
import random
import time
from typing import Dict, Any, Optional, Union

from ..client import ConvoAIClient
from ..config import Config, ServiceRegion
from ..auth import BasicAuthCredential
from .token import TokenBuilder
from .property import PropertyBuilder
from .components import BaseASRConfig, BaseLLMConfig, BaseTTSConfig


class AgentClient:
    """Handles business logic and API calls for agent operations"""
    
    def __init__(
        self,
        app_id: str,
        app_certificate: str,
        customer_id: str,
        customer_secret: str
    ):
        """
        Initialize AgentClient with configuration
        
        Args:
            app_id: Agora App ID
            app_certificate: Agora App Certificate
            customer_id: Agora Customer ID (API Key)
            customer_secret: Agora Customer Secret (API Secret)
        
        Example:
            client = AgentClient(
                app_id=os.getenv("APP_ID"),
                app_certificate=os.getenv("APP_CERTIFICATE"),
                customer_id=os.getenv("API_KEY"),
                customer_secret=os.getenv("API_SECRET")
            )
        """
        if not all([app_id, app_certificate, customer_id, customer_secret]):
            raise ValueError(
                "All parameters are required: "
                "app_id, app_certificate, customer_id, customer_secret"
            )
        
        self.app_id = app_id
        self.app_certificate = app_certificate
        self.customer_id = customer_id
        self.customer_secret = customer_secret
        self._client = None
    
    def _get_client(self) -> ConvoAIClient:
        """Get or create ConvoAIClient instance"""
        if self._client is None:
            client_config = Config(
                app_id=self.app_id,
                credential=BasicAuthCredential(
                    self.customer_id,
                    self.customer_secret
                ),
                service_region=ServiceRegion.CHINESE_MAINLAND,
                http_timeout=60,
                retry_count=3
            )
            self._client = ConvoAIClient(client_config)
        return self._client
    
    def build_agent_properties(
        self,
        channel: str,
        agent_uid: str,
        user_uid: str,
        token: str,
        asr_config: Dict[str, Any],
        llm_config: Dict[str, Any],
        tts_config: Dict[str, Any]
    ):
        """Build agent properties with ASR, LLM, and TTS configuration"""
        return PropertyBuilder.build_join_properties(
            channel=channel,
            agent_uid=agent_uid,
            user_uid=user_uid,
            token=token,
            asr_config=asr_config,
            llm_config=llm_config,
            tts_config=tts_config
        )
    
    def start_agent(
        self,
        channel_name: str,
        agent_uid: str,
        user_uid: str,
        asr_config: Union[BaseASRConfig, Dict[str, Any]],
        llm_config: Union[BaseLLMConfig, Dict[str, Any]],
        tts_config: Union[BaseTTSConfig, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Start agent with ASR, LLM, and TTS configuration
        
        Args:
            channel_name: RTC channel name
            agent_uid: Agent's RTC UID
            user_uid: User's RTC UID
            asr_config: ASR configuration (config object or dict)
            llm_config: LLM configuration (config object or dict)
            tts_config: TTS configuration (config object or dict)
        
        Returns:
            Dict containing agent_id, channel_name, and status
        
        Examples:
            # Using config objects
            result = client.start_agent(
                channel_name="my_channel",
                agent_uid="123456",
                user_uid="789012",
                asr_config=DeepgramASRConfig(api_key="xxx"),
                llm_config=OpenAILLMConfig(api_key="yyy"),
                tts_config=ElevenLabsTTSConfig(api_key="zzz")
            )
            
            # Using dictionaries
            result = client.start_agent(
                channel_name="my_channel",
                agent_uid="123456",
                user_uid="789012",
                asr_config={"vendor": "deepgram", "api_key": "xxx"},
                llm_config={"api_key": "yyy", "model": "gpt-4"},
                tts_config={"vendor": "elevenlabs", "api_key": "zzz"}
            )
        """
        # Convert config objects to dictionaries if needed
        asr_dict = asr_config.to_dict() if hasattr(asr_config, 'to_dict') else asr_config
        llm_dict = llm_config.to_dict() if hasattr(llm_config, 'to_dict') else llm_config
        tts_dict = tts_config.to_dict() if hasattr(tts_config, 'to_dict') else tts_config
        
        # Generate Agent Token
        agent_token = TokenBuilder.generate(
            app_id=self.app_id,
            app_certificate=self.app_certificate,
            channel_name=channel_name,
            uid=agent_uid
        )
        
        # Build Agent configuration
        properties = self.build_agent_properties(
            channel=channel_name,
            agent_uid=agent_uid,
            user_uid=user_uid,
            token=agent_token,
            asr_config=asr_dict,
            llm_config=llm_dict,
            tts_config=tts_dict
        )
        
        # Call join API
        name = f"{self.app_id}:{channel_name}"
        
        response = self._get_client().join(name, properties)
        
        if response.success_resp:
            return {
                "agent_id": response.success_resp.agent_id,
                "channel_name": channel_name,
                "status": "started"
            }
        else:
            error_msg = "Unknown error"
            if response.err_response:
                error_msg = f"{response.err_response.reason}: {response.err_response.detail}"
            raise RuntimeError(f"Failed to start agent: {error_msg}")
    
    def stop_agent(self, agent_id: str) -> None:
        """Stop agent by agent_id"""
        self._get_client().leave(agent_id)

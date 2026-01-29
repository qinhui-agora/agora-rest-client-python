"""
Agent Manager

Handles business logic and API calls for Agora Conversational AI Agents.
"""
import json
import random
import time
from typing import Dict, Any, Optional

from ..client import ConvoAIClient
from ..config import Config, ServiceRegion
from ..auth import BasicAuthCredential
from .config import AgentConfig
from .token import TokenBuilder
from .property import PropertyBuilder


class AgentManager:
    """Handles business logic and API calls for agent operations"""
    
    def __init__(self, config: AgentConfig):
        """Initialize AgentManager with configuration"""
        self.config = config
        self._client = None
    
    def _get_client(self) -> ConvoAIClient:
        """Get or create ConvoAIClient instance"""
        if self._client is None:
            client_config = Config(
                app_id=self.config.app_id,
                credential=BasicAuthCredential(
                    self.config.customer_id,
                    self.config.customer_secret
                ),
                service_region=ServiceRegion.CHINESE_MAINLAND,
                http_timeout=60,
                retry_count=3
            )
            self._client = ConvoAIClient(client_config)
        return self._client
    
    def generate_config(self) -> Dict[str, Any]:
        """Generate connection configuration with token, channel, and UIDs"""
        # Generate UIDs
        user_uid = random.randint(1000, 9999999)
        agent_uid = random.randint(10000000, 99999999)
        
        # Generate channel name
        channel_name = f"channel_{int(time.time())}"
        
        # Generate token for user
        token = TokenBuilder.generate(
            app_id=self.config.app_id,
            app_certificate=self.config.app_certificate,
            channel_name=channel_name,
            uid=str(user_uid)
        )
        
        return {
            "app_id": self.config.app_id,
            "token": token,
            "uid": str(user_uid),
            "channel_name": channel_name,
            "agent_uid": str(agent_uid)
        }
    
    def generate_agent_token(
        self,
        channel_name: str,
        agent_uid: str,
        expire: int = 86400
    ) -> str:
        """Generate RTC token for agent"""
        return TokenBuilder.generate(
            app_id=self.config.app_id,
            app_certificate=self.config.app_certificate,
            channel_name=channel_name,
            uid=agent_uid,
            expire=expire
        )
    
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
        asr_config: Dict[str, Any],
        llm_config: Dict[str, Any],
        tts_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start agent with ASR, LLM, and TTS configuration"""
        # Generate Agent Token
        agent_token = self.generate_agent_token(channel_name, agent_uid)
        
        # Build Agent configuration
        properties = self.build_agent_properties(
            channel=channel_name,
            agent_uid=agent_uid,
            user_uid=user_uid,
            token=agent_token,
            asr_config=asr_config,
            llm_config=llm_config,
            tts_config=tts_config
        )
        
        # Call join API
        name = f"{self.config.app_id}:{channel_name}"
        
        print("\n" + "="*80)
        print("JOIN API REQUEST DEBUG")
        print("="*80)
        print(f"Name: {name}")
        print(f"Properties: {json.dumps(properties.dict(exclude_none=True, by_alias=True), indent=2)}")
        print("="*80 + "\n")
        
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

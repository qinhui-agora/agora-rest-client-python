"""
Agora Conversational AI Client

Corresponds to Go version: agora-rest-client-go/services/convoai/client.go
"""
from typing import Optional

from .config import Config
from .api.join import JoinAPI
from .api.leave import LeaveAPI
from .req.join import JoinPropertiesReqBody
from .resp.join import JoinResp
from .resp.leave import LeaveResp


class ConvoAIClient:
    """
    Conversational AI engine client
    
    Provides methods to interact with Agora Conversational AI API:
    - join: Create an agent instance and join RTC channel
    - leave: Stop an agent instance and leave RTC channel
    
    Example:
        ```python
        from agora_convoai import ConvoAIClient, Config, ServiceRegion, BasicAuthCredential
        
        # Create configuration
        config = Config(
            app_id="your_app_id",
            credential=BasicAuthCredential("customer_id", "customer_secret"),
            service_region=ServiceRegion.GLOBAL
        )
        
        # Create client
        client = ConvoAIClient(config)
        
        # Join - create agent
        from agora_convoai.req import JoinPropertiesReqBody
        
        properties = JoinPropertiesReqBody(
            channel="test_channel",
            token="your_rtc_token",
            agent_rtc_uid="123456",
            remote_rtc_uids=["789012"],
            # ... other configurations
        )
        
        response = client.join(name="agent_name", properties=properties)
        if response.is_success():
            print(f"Agent ID: {response.success_resp.agent_id}")
        
        # Leave - stop agent
        leave_resp = client.leave(agent_id=response.success_resp.agent_id)
        if leave_resp.is_success():
            print("Agent stopped successfully")
        ```
    
    @since v0.7.0
    """
    
    def __init__(self, config: Config):
        """
        Initialize Conversational AI client
        
        Args:
            config: Configuration instance containing app_id, credential, service_region, etc.
        
        Raises:
            ValidationError: If configuration is invalid
        """
        self.config = config
        
        # Get prefix path based on service region
        prefix_path = config.get_prefix_path()
        
        # Initialize API handlers
        self._join_api = JoinAPI(
            module="convoai:join",
            logger=config.logger,
            retry_count=config.retry_count,
            config=config,
            prefix_path=prefix_path
        )
        
        self._leave_api = LeaveAPI(
            module="convoai:leave",
            logger=config.logger,
            retry_count=config.retry_count,
            config=config,
            prefix_path=prefix_path
        )
    
    def join(
        self,
        name: str,
        properties: JoinPropertiesReqBody
    ) -> JoinResp:
        """
        Create an agent instance and join the specified RTC channel
        
        @since v0.7.0
        
        Example:
            Use this to create an agent instance in an RTC channel.
        
        Post-condition:
            After successful execution, the agent will join the specified channel.
            You can perform subsequent operations using the returned agent ID.
        
        Args:
            name: Unique identifier for the agent. The same identifier cannot be used repeatedly.
            properties: Configuration properties of the agent, including channel information,
                       token, LLM settings, TTS settings, etc.
        
        Returns:
            JoinResp containing:
            - success_resp: JoinSuccessResp with agent_id, create_ts, and status (if successful)
            - err_response: ErrResponse with error details (if failed)
        
        Raises:
            AgoraAPIError: If request fails with client error (4xx)
            RetryError: If all retry attempts fail
            ValidationError: If parameters are invalid
        
        Example:
            ```python
            from agora_convoai.req import (
                JoinPropertiesReqBody,
                JoinPropertiesCustomLLMBody,
                JoinPropertiesTTSBody,
                TTSVendor,
                TTSMicrosoftVendorParams
            )
            
            # Configure LLM
            llm_config = JoinPropertiesCustomLLMBody(
                url="https://api.openai.com/v1/chat/completions",
                api_key="your_api_key",
                system_messages=[{"role": "system", "content": "You are a helpful assistant."}],
                params={"model": "gpt-4", "max_tokens": 2048}
            )
            
            # Configure TTS
            tts_config = JoinPropertiesTTSBody(
                vendor=TTSVendor.MICROSOFT,
                params=TTSMicrosoftVendorParams(
                    key="your_key",
                    region="eastus",
                    voice_name="en-US-JennyNeural",
                    speed=1.0,
                    volume=70
                )
            )
            
            # Create properties
            properties = JoinPropertiesReqBody(
                channel="my_channel",
                token="rtc_token",
                agent_rtc_uid="123456",
                remote_rtc_uids=["789012"],
                llm=llm_config,
                tts=tts_config
            )
            
            # Join
            response = client.join(name="my_agent", properties=properties)
            
            if response.is_success():
                print(f"Agent created: {response.success_resp.agent_id}")
                print(f"Status: {response.success_resp.status}")
            else:
                print(f"Error: {response.err_response.detail}")
            ```
        """
        return self._join_api.do(name=name, properties_body=properties)
    
    def leave(self, agent_id: str) -> LeaveResp:
        """
        Stop the specified agent instance and leave the RTC channel
        
        @since v0.7.0
        
        Example:
            Use this to stop an agent instance.
        
        Post-condition:
            After successful execution, the agent will be stopped and leave the RTC channel.
        
        Note:
            Ensure the agent ID has been obtained by calling the join() method before using this method.
        
        Args:
            agent_id: Agent ID obtained from join() response
        
        Returns:
            LeaveResp containing:
            - base_response: BaseResponse with HTTP status code
            - err_response: ErrResponse with error details (if failed)
        
        Raises:
            AgoraAPIError: If request fails with client error (4xx)
            RetryError: If all retry attempts fail
        
        Example:
            ```python
            # Stop agent
            response = client.leave(agent_id="agent_123")
            
            if response.is_success():
                print("Agent stopped successfully")
            else:
                print(f"Error: {response.err_response.detail}")
            ```
        """
        return self._leave_api.do(agent_id=agent_id)

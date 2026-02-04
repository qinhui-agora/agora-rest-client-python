"""
Low-level API usage example for Agora REST Client Python

Demonstrates direct usage of the ConvoAIClient without the high-level AgentClient.
This example shows:
1. Creating a client with configuration
2. Joining an agent with custom TTS configuration
3. Leaving the agent

This approach gives you full control over the API calls and configurations.

Note: Currently only join() and leave() APIs are implemented.
"""
import os
import time
import logging
from agora_rest import ConvoAIClient, Config, ServiceRegion, BasicAuthCredential
from agora_rest.req.join import (
    JoinPropertiesReqBody,
    JoinPropertiesCustomLLMBody,
    JoinPropertiesTTSBody,
    JoinPropertiesAsrBody,
    JoinPropertiesAdvancedFeaturesBody,
    TTSVendor,
    TTSElevenLabsVendorParams,
    Parameters,
    FixedParams,
    SilenceConfig,
)


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_client() -> ConvoAIClient:
    """
    Create and configure ConvoAI client
    
    Returns:
        Configured ConvoAIClient instance
    """
    # Load configuration from environment
    app_id = os.getenv("APP_ID")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    
    if not app_id:
        raise ValueError("APP_ID is required")
    if not api_key:
        raise ValueError("API_KEY is required")
    if not api_secret:
        raise ValueError("API_SECRET is required")
    
    # Create credential
    credential = BasicAuthCredential(api_key, api_secret)
    
    # Create configuration
    config = Config(
        app_id=app_id,
        credential=credential,
        service_region=ServiceRegion.GLOBAL,
        http_timeout=20,
        retry_count=3,
        logger=logger
    )
    
    # Create client
    client = ConvoAIClient(config)
    
    logger.info("✓ ConvoAI client created")
    return client


def run_with_elevenlabs_tts(client: ConvoAIClient):
    """
    Run agent with ElevenLabs TTS
    
    Args:
        client: ConvoAIClient instance
    """
    # Load environment variables
    rtc_token = os.getenv("RTC_TOKEN")
    channel = os.getenv("CHANNEL", "test_channel")
    agent_uid = os.getenv("AGENT_UID", "123456")
    user_uid = os.getenv("USER_UID", "789012")
    
    llm_api_key = os.getenv("LLM_API_KEY")
    tts_api_key = os.getenv("TTS_ELEVENLABS_API_KEY")
    
    # Validate required variables
    if not rtc_token:
        raise ValueError("RTC_TOKEN is required")
    if not llm_api_key:
        raise ValueError("LLM_API_KEY is required")
    if not tts_api_key:
        raise ValueError("TTS_ELEVENLABS_API_KEY is required")
    
    # Configure TTS (ElevenLabs)
    tts_params = TTSElevenLabsVendorParams(
        key=tts_api_key,
        model_id="eleven_multilingual_v2",
        voice_id="pNInz6obpgDQGcFmaJgB"
    )
    
    run_with_custom_tts(
        client=client,
        rtc_token=rtc_token,
        channel=channel,
        agent_uid=agent_uid,
        user_uid=user_uid,
        llm_api_key=llm_api_key,
        tts_vendor=TTSVendor.ELEVENLABS,
        tts_params=tts_params
    )


def run_with_custom_tts(
    client: ConvoAIClient,
    rtc_token: str,
    channel: str,
    agent_uid: str,
    user_uid: str,
    llm_api_key: str,
    tts_vendor: TTSVendor,
    tts_params
):
    """
    Run agent with custom TTS configuration
    
    This function demonstrates the basic lifecycle of an agent:
    1. Join - create and start agent
    2. Agent runs and processes audio/conversations
    3. Leave - stop and cleanup agent
    
    Args:
        client: ConvoAIClient instance
        rtc_token: RTC token
        channel: Channel name
        agent_uid: Agent RTC UID
        user_uid: User RTC UID
        llm_api_key: LLM API key
        tts_vendor: TTS vendor
        tts_params: TTS vendor parameters
    """
    # Generate unique agent name
    agent_name = f"{client.config.app_id}:{channel}"
    
    # Configure LLM (OpenAI)
    llm_config = JoinPropertiesCustomLLMBody(
        url="https://api.openai.com/v1/chat/completions",
        api_key=llm_api_key,
        system_messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ],
        params={
            "model": "gpt-4",
            "max_tokens": 1024
        },
        max_history=30,
        greeting_message="Hello, how can I help you?"
    )
    
    # Configure TTS
    tts_config = JoinPropertiesTTSBody(
        vendor=tts_vendor,
        params=tts_params
    )
    
    # Configure ASR (optional - uses default if not provided)
    asr_config = None
    deepgram_key = os.getenv("ASR_DEEPGRAM_API_KEY")
    if deepgram_key:
        asr_config = JoinPropertiesAsrBody(
            language="en-US"
        )
    
    # Configure advanced features
    advanced_features = JoinPropertiesAdvancedFeaturesBody(
        enable_aivad=True
    )
    
    # Configure parameters
    parameters = Parameters(
        fixed_params=FixedParams(
            silence_config=SilenceConfig(
                timeout_ms=1200,
                action="speak",
                content="Hello, how can I help you?"
            )
        )
    )
    
    # Create join properties
    properties = JoinPropertiesReqBody(
        token=rtc_token,
        channel=channel,
        agent_rtc_uid=agent_uid,
        remote_rtc_uids=[user_uid],
        enable_string_uid=False,
        idle_timeout=120,
        advanced_features=advanced_features,
        llm=llm_config,
        tts=tts_config,
        asr=asr_config,
        parameters=parameters
    )
    
    # 1. Join - create agent
    logger.info(f"🚀 Starting agent in channel '{channel}'...")
    join_resp = client.join(name=agent_name, properties=properties)
    
    if not join_resp.is_success():
        logger.error(f"✗ Join failed: {join_resp.err_response.dict()}")
        return
    
    logger.info(f"✓ Join success: {join_resp.success_resp.dict()}")
    agent_id = join_resp.success_resp.agent_id
    
    try:
        # 2. Agent is now running
        logger.info(f"✅ Agent {agent_id} is running in channel '{channel}'")
        logger.info("💡 The agent will:")
        logger.info("   - Listen to audio from remote users")
        logger.info("   - Process speech through ASR")
        logger.info("   - Generate responses using LLM")
        logger.info("   - Speak responses using TTS")
        
        # Keep agent running for a while (simulate real usage)
        logger.info("⏳ Agent will run for 10 seconds...")
        time.sleep(10)
        
    finally:
        # 3. Leave - stop agent
        logger.info(f"🛑 Stopping agent {agent_id}...")
        leave_resp = client.leave(agent_id)
        
        if leave_resp.is_success():
            logger.info("✓ Leave success")
        else:
            logger.error(f"✗ Leave failed: {leave_resp.err_response.dict()}")


def main():
    """Main function"""
    try:
        # Create client
        client = create_client()
        
        # Run with ElevenLabs TTS
        # TODO: Add support for other TTS providers (Microsoft, etc.)
        logger.info("Using ElevenLabs TTS")
        run_with_elevenlabs_tts(client)
        
        logger.info("✅ Example completed successfully!")
        
    except ValueError as e:
        logger.error(f"✗ Configuration error: {e}")
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

"""
Basic usage example for Agora REST Client Python

Demonstrates how to use the high-level Agent API:
1. Create AgentClient
2. Generate channel, UIDs, and token
3. Start an agent
4. Stop the agent
"""
import os
import sys
import random

# Add parent directory to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Try to load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agora_rest.agent import (
    AgentClient,
    TokenBuilder,
    DeepgramASRConfig,
    OpenAILLMConfig,
    ElevenLabsTTSConfig
)


def main():
    """Main example function"""
    
    # Load Agora credentials from environment
    app_id = os.getenv("APP_ID")
    app_certificate = os.getenv("APP_CERTIFICATE")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    
    if not all([app_id, app_certificate, api_key, api_secret]):
        raise ValueError("Missing required Agora credentials in environment variables")
    
    print("✓ Agora credentials loaded")
    
    # Create agent client
    client = AgentClient(
        app_id=app_id,
        app_certificate=app_certificate,
        customer_id=api_key,
        customer_secret=api_secret
    )
    
    print("✓ Agent client created")
    
    # Generate connection configuration
    import uuid
    channel_name = f"channel_{uuid.uuid4().hex[:8]}"
    user_uid = str(random.randint(100000, 999999))
    agent_uid = str(random.randint(100000, 999999))
    
    # Generate token for agent
    token = TokenBuilder.generate(
        app_id=app_id,
        app_certificate=app_certificate,
        channel_name=channel_name,
        uid=agent_uid
    )
    
    print("\n📋 Connection Configuration:")
    print(f"  - App ID: {app_id}")
    print(f"  - Channel: {channel_name}")
    print(f"  - User UID: {user_uid}")
    print(f"  - Agent UID: {agent_uid}")
    print(f"  - Token: {token[:20]}...")
    
    # Configure ASR (Deepgram)
    asr_api_key = os.getenv("ASR_DEEPGRAM_API_KEY")
    asr = DeepgramASRConfig(api_key=asr_api_key)
    
    # Configure LLM (OpenAI)
    llm_api_key = os.getenv("LLM_API_KEY")
    llm = OpenAILLMConfig(api_key=llm_api_key)
    
    # Configure TTS (ElevenLabs)
    tts_api_key = os.getenv("TTS_ELEVENLABS_API_KEY")
    tts = ElevenLabsTTSConfig(api_key=tts_api_key)
    
    # Optional: Customize configurations
    # llm.model = "gpt-4o"
    # llm.system_message = "You are a helpful AI assistant."
    # llm.greeting = "Hello! How can I help you today?"
    # asr.model = "nova-2"
    # asr.language = "zh-CN"
    # tts.voice_id = "your_custom_voice_id"
    
    print("\n✓ ASR, LLM, TTS configured")
    
    # Start the agent
    print(f"\n🚀 Starting agent in channel '{channel_name}'...")
    
    try:
        result = client.start_agent(
            channel_name=channel_name,
            agent_uid=agent_uid,
            user_uid=user_uid,
            asr_config=asr,
            llm_config=llm,
            tts_config=tts
        )
        
        agent_id = result['agent_id']
        print(f"✓ Agent started successfully!")
        print(f"  - Agent ID: {agent_id}")
        print(f"  - Channel: {result['channel_name']}")
        print(f"  - Status: {result['status']}")
        
        # Stop the agent
        print(f"\n🛑 Stopping agent {agent_id}...")
        client.stop_agent(agent_id)
        print("✓ Agent stopped successfully!")
        
    except ValueError as e:
        print(f"✗ Validation error: {e}")
    except RuntimeError as e:
        print(f"✗ Runtime error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

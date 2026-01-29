"""
Basic usage example for Agora REST Client Python

Demonstrates how to use the high-level Agent API:
1. Load configuration from environment
2. Generate connection config (token, channel, UIDs)
3. Start an agent
4. Stop the agent
"""
import os
from agora_rest import AgentConfig, AgentManager
from agora_rest.agent import ASRConfig, LLMConfig, TTSConfig


def main():
    """Main example function"""
    
    # Load configuration from environment variables
    # Automatically loads .env or .env.local if available
    config = AgentConfig.from_env()
    
    print("✓ Configuration loaded")
    
    # Create agent manager
    manager = AgentManager(config)
    
    print("✓ Agent manager created")
    
    # Generate connection configuration
    # This creates: token, channel_name, user UID, agent UID
    config_data = manager.generate_config()
    
    print("\n📋 Connection Configuration:")
    print(f"  - App ID: {config_data['app_id']}")
    print(f"  - Channel: {config_data['channel_name']}")
    print(f"  - User UID: {config_data['uid']}")
    print(f"  - Agent UID: {config_data['agent_uid']}")
    print(f"  - Token: {config_data['token'][:20]}...")
    
    # Configure ASR (Deepgram) - uses default model and language
    asr = ASRConfig(api_key=config.deepgram_api_key)
    
    # Configure LLM (OpenAI) - uses default model, system message, and greeting
    llm = LLMConfig(api_key=config.llm_api_key)
    
    # Configure TTS (ElevenLabs) - uses default model and voice
    tts = TTSConfig(api_key=config.tts_elevenlabs_api_key)
    
    # Optional: Customize configurations
    # llm.model = "gpt-4o"
    # llm.system_message = "You are a helpful AI assistant."
    # llm.greeting = "Hello! How can I help you today?"
    # asr.model = "nova-2"
    # asr.language = "zh-CN"
    # tts.voice_id = "your_custom_voice_id"
    
    print("\n✓ ASR, LLM, TTS configured with defaults")
    
    # Start the agent
    print(f"\n🚀 Starting agent in channel '{config_data['channel_name']}'...")
    
    try:
        result = manager.start_agent(
            channel_name=config_data['channel_name'],
            agent_uid=config_data['agent_uid'],
            user_uid=config_data['uid'],
            asr_config=asr.to_dict(),
            llm_config=llm.to_dict(),
            tts_config=tts.to_dict()
        )
        
        agent_id = result['agent_id']
        print(f"✓ Agent started successfully!")
        print(f"  - Agent ID: {agent_id}")
        print(f"  - Channel: {result['channel_name']}")
        print(f"  - Status: {result['status']}")
        
        # Stop the agent
        print(f"\n🛑 Stopping agent {agent_id}...")
        manager.stop_agent(agent_id)
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

"""
Manual test script for quick validation

This script tests the complete agent lifecycle:
1. Create AgentClient
2. Generate connection configuration
3. Start agent
4. Stop agent

Usage:
    # Set environment variables in .env file or export them
    python tests/manual_test.py

Required environment variables:
    APP_ID, APP_CERTIFICATE, API_KEY, API_SECRET, LLM_API_KEY
    ASR_DEEPGRAM_API_KEY (optional), TTS_ELEVENLABS_API_KEY (optional)
"""
import os
import sys
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agora_rest import AgentClient
from agora_rest.agent import DeepgramASRConfig, OpenAILLMConfig, ElevenLabsTTSConfig


def load_env():
    """Load environment variables from .env file if available"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed, use system environment variables


def check_credentials():
    """Check if all required credentials are set"""
    required = {
        "APP_ID": os.getenv("APP_ID"),
        "APP_CERTIFICATE": os.getenv("APP_CERTIFICATE"),
        "API_KEY": os.getenv("API_KEY"),
        "API_SECRET": os.getenv("API_SECRET"),
        "LLM_API_KEY": os.getenv("LLM_API_KEY"),
    }
    
    optional = {
        "ASR_DEEPGRAM_API_KEY": os.getenv("ASR_DEEPGRAM_API_KEY"),
        "TTS_ELEVENLABS_API_KEY": os.getenv("TTS_ELEVENLABS_API_KEY"),
    }
    
    print("\nChecking credentials...")
    
    missing = []
    for key, value in required.items():
        if value:
            print(f"  ✓ {key}")
        else:
            print(f"  ✗ {key}: NOT SET")
            missing.append(key)
    
    for key, value in optional.items():
        if value:
            print(f"  ✓ {key} (optional)")
        else:
            print(f"  - {key}: NOT SET (optional)")
    
    if missing:
        print(f"\nMissing required credentials: {', '.join(missing)}")
        return False
    
    return True


def test_agent_lifecycle():
    """Test complete agent lifecycle"""
    print("\n" + "="*60)
    print("Testing Agent Lifecycle")
    print("="*60)
    
    # Create client
    print("\n1. Creating AgentClient...")
    client = AgentClient(
        app_id=os.getenv("APP_ID"),
        app_certificate=os.getenv("APP_CERTIFICATE"),
        customer_id=os.getenv("API_KEY"),
        customer_secret=os.getenv("API_SECRET")
    )
    print("   ✓ Client created")
    
    # Generate config
    print("\n2. Generating connection configuration...")
    config_data = client.generate_config()
    print(f"   ✓ Channel: {config_data['channel_name']}")
    print(f"   ✓ User UID: {config_data['uid']}")
    print(f"   ✓ Agent UID: {config_data['agent_uid']}")
    
    # Configure components
    print("\n3. Configuring ASR, LLM, TTS...")
    asr = DeepgramASRConfig(api_key=os.getenv("ASR_DEEPGRAM_API_KEY"))
    llm = OpenAILLMConfig(api_key=os.getenv("LLM_API_KEY"))
    tts = ElevenLabsTTSConfig(api_key=os.getenv("TTS_ELEVENLABS_API_KEY"))
    print("   ✓ Components configured")
    
    # Start agent
    print(f"\n4. Starting agent...")
    try:
        result = client.start_agent(
            channel_name=config_data['channel_name'],
            agent_uid=config_data['agent_uid'],
            user_uid=config_data['uid'],
            asr_config=asr,
            llm_config=llm,
            tts_config=tts
        )
        
        agent_id = result['agent_id']
        print(f"   ✓ Agent started: {agent_id}")
        
        # Keep agent running
        print(f"\n5. Agent running (5 seconds)...")
        time.sleep(5)
        
        # Stop agent
        print(f"\n6. Stopping agent...")
        client.stop_agent(agent_id)
        print(f"   ✓ Agent stopped")
        
        print("\n" + "="*60)
        print("✅ TEST PASSED")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n   ✗ Error: {e}")
        print("\n" + "="*60)
        print("❌ TEST FAILED")
        print("="*60)
        return False


def main():
    """Main test function"""
    print("Agora REST Client - Manual Test")
    
    # Load environment
    load_env()
    
    # Check credentials
    if not check_credentials():
        print("\nTip: Create a .env file with your credentials")
        return 1
    
    # Run test
    success = test_agent_lifecycle()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

"""
Agent Configuration Management

Loads configuration from environment variables for agent operations.
"""
import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

# Try to import dotenv, but make it optional
try:
    from dotenv import load_dotenv
    _HAS_DOTENV = True
except ImportError:
    _HAS_DOTENV = False


@dataclass
class AgentConfig:
    """Agent configuration loaded from environment variables"""
    
    # Agora credentials
    app_id: str
    app_certificate: str
    customer_id: str
    customer_secret: str
    
    # LLM configuration - OpenAI
    llm_api_key: str
    
    # TTS configuration - ElevenLabs
    tts_elevenlabs_api_key: Optional[str] = None
    
    # ASR configuration - Deepgram
    deepgram_api_key: Optional[str] = None
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None, auto_load_dotenv: bool = True) -> 'AgentConfig':
        """Load configuration from environment variables"""
        # Auto-load .env files if dotenv is available
        if auto_load_dotenv and _HAS_DOTENV:
            if env_file:
                load_dotenv(env_file, override=False)
            else:
                # Try to find .env files in common locations
                cwd = Path.cwd()
                for env_name in ['.env.local', '.env']:
                    env_path = cwd / env_name
                    if env_path.exists():
                        load_dotenv(env_path, override=False)
                        break
                
                parent = cwd.parent
                for env_name in ['.env.local', '.env']:
                    env_path = parent / env_name
                    if env_path.exists():
                        load_dotenv(env_path, override=False)
                        break
        
        def get_env(key: str) -> str:
            """Get environment variable with prefix fallbacks"""
            value = os.getenv(f"VITE_AG_{key}")
            if value:
                return value
            
            value = os.getenv(f"AGORA_{key}")
            if value:
                return value
            
            value = os.getenv(key)
            if value:
                return value
            
            # Special mapping: API_KEY/API_SECRET -> CUSTOMER_ID/CUSTOMER_SECRET
            if key == "CUSTOMER_ID":
                return os.getenv("API_KEY") or ""
            elif key == "CUSTOMER_SECRET":
                return os.getenv("API_SECRET") or ""
            
            return ""
        
        # Required Agora credentials
        app_id = get_env("APP_ID")
        app_certificate = get_env("APP_CERTIFICATE")
        customer_id = get_env("CUSTOMER_ID")
        customer_secret = get_env("CUSTOMER_SECRET")
        
        if not all([app_id, app_certificate, customer_id, customer_secret]):
            raise ValueError(
                "Missing required Agora configuration: "
                "APP_ID, APP_CERTIFICATE, CUSTOMER_ID (or API_KEY), CUSTOMER_SECRET (or API_SECRET)"
            )
        
        # Required LLM configuration
        llm_api_key = os.getenv("LLM_API_KEY")
        
        if not llm_api_key:
            raise ValueError("Missing required LLM configuration: LLM_API_KEY")
        
        return cls(
            app_id=app_id,
            app_certificate=app_certificate,
            customer_id=customer_id,
            customer_secret=customer_secret,
            llm_api_key=llm_api_key,
            tts_elevenlabs_api_key=os.getenv("TTS_ELEVENLABS_API_KEY"),
            deepgram_api_key=os.getenv("ASR_DEEPGRAM_API_KEY"),
        )

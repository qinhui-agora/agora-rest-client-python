"""
Agora Conversational AI API Configuration Module
"""
from enum import Enum
from typing import Optional
import logging

from .auth import Credential
from .exceptions import ValidationError


class ServiceRegion(Enum):
    """
    Service region enumeration
    
    Chinese Mainland and Global regions are two different services
    """
    UNKNOWN = 0
    CHINESE_MAINLAND = 1  # Chinese Mainland service region
    GLOBAL = 2  # Global service region (excluding Chinese Mainland)


class Config:
    """
    Conversational AI client configuration class
    
    Contains all configuration information needed to connect to Agora Conversational AI service
    """
    
    # Default timeout (seconds)
    DEFAULT_TIMEOUT = 60
    # Default retry count
    DEFAULT_RETRY_COUNT = 3
    
    def __init__(
        self,
        app_id: str,
        credential: Credential,
        service_region: ServiceRegion = ServiceRegion.GLOBAL,
        http_timeout: int = DEFAULT_TIMEOUT,
        retry_count: int = DEFAULT_RETRY_COUNT,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize configuration
        
        Args:
            app_id: Agora App ID
            credential: Authentication credential (e.g., BasicAuthCredential)
            service_region: Service region (Chinese Mainland or Global)
            http_timeout: HTTP request timeout (seconds)
            retry_count: Number of retry attempts on failure
            logger: Logger instance (optional, defaults to standard library logging)
        
        Raises:
            ValidationError: Parameter validation failure
        """
        # Validate required parameters
        if not app_id:
            raise ValidationError("app_id cannot be empty")
        if not credential:
            raise ValidationError("credential cannot be empty")
        if service_region == ServiceRegion.UNKNOWN:
            raise ValidationError("service_region cannot be UNKNOWN")
        
        self.app_id = app_id
        self.credential = credential
        self.service_region = service_region
        self.http_timeout = http_timeout
        self.retry_count = retry_count
        
        # Setup logger
        if logger is None:
            self.logger = logging.getLogger("agora_convoai")
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger
    
    def get_base_url(self) -> str:
        """
        Get base URL based on service region
        
        Returns:
            API base URL
        """
        if self.service_region == ServiceRegion.CHINESE_MAINLAND:
            return "https://api.agora.io/cn"
        elif self.service_region == ServiceRegion.GLOBAL:
            return "https://api.agora.io"
        else:
            raise ValidationError(f"Unsupported service region: {self.service_region}")
    
    def get_prefix_path(self) -> str:
        """
        Get API path prefix
        
        Returns:
            API path prefix, e.g.: /api/conversational-ai-agent/v2/projects/{app_id}
        """
        # Note: base_url already includes /cn for CHINESE_MAINLAND, so don't duplicate it
        return f"/api/conversational-ai-agent/v2/projects/{self.app_id}"

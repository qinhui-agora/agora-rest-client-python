"""
Agora Conversational AI API Authentication Module
"""
from abc import ABC, abstractmethod
from typing import Dict


class Credential(ABC):
    """Base class for authentication credentials"""
    
    @abstractmethod
    def get_auth_header(self) -> Dict[str, str]:
        """
        Get authentication request headers
        
        Returns:
            Dictionary containing authentication information
        """
        pass


class BasicAuthCredential(Credential):
    """
    Basic Auth credential
    
    Uses customer ID and customer secret for HTTP Basic Authentication
    """
    
    def __init__(self, customer_id: str, customer_secret: str):
        """
        Initialize Basic Auth credential
        
        Args:
            customer_id: Customer ID (corresponds to RESTful API Customer ID)
            customer_secret: Customer Secret (corresponds to RESTful API Customer Secret)
        """
        if not customer_id or not customer_secret:
            raise ValueError("customer_id and customer_secret cannot be empty")
        
        self.customer_id = customer_id
        self.customer_secret = customer_secret
    
    def get_auth_header(self) -> Dict[str, str]:
        """
        Get Basic Auth request headers
        
        Returns:
            Dictionary containing Authorization header
        """
        import base64
        
        credentials = f"{self.customer_id}:{self.customer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            "Authorization": f"Basic {encoded_credentials}"
        }

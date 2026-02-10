"""
Agora REST Client - Python SDK

Python client for Agora REST APIs including Conversational AI.
"""

__version__ = "0.1.3"

from .auth import Credential, BasicAuthCredential
from .config import Config, ServiceRegion
from .exceptions import (
    AgoraAPIError,
    AuthenticationError,
    RetryError,
    ValidationError,
    TimeoutError,
)
from .resp import (
    BaseResponse,
    ErrResponse,
    Response,
    JoinSuccessResp,
    JoinResp,
    LeaveResp,
)
from .client import ConvoAIClient

__all__ = [
    # Version
    "__version__",
    # Authentication
    "Credential",
    "BasicAuthCredential",
    # Configuration
    "Config",
    "ServiceRegion",
    # Exceptions
    "AgoraAPIError",
    "AuthenticationError",
    "RetryError",
    "ValidationError",
    "TimeoutError",
    # Response Models
    "BaseResponse",
    "ErrResponse",
    "Response",
    "JoinSuccessResp",
    "JoinResp",
    "LeaveResp",
    # Client
    "ConvoAIClient",
]

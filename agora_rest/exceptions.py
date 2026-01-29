"""
Agora Conversational AI API Exception Definitions
"""


class AgoraAPIError(Exception):
    """Base exception class for Agora API"""
    
    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(AgoraAPIError):
    """Authentication failure exception"""
    pass


class RetryError(AgoraAPIError):
    """Retry failure exception"""
    
    def __init__(self, message: str, retry_count: int, last_error: Exception = None):
        self.retry_count = retry_count
        self.last_error = last_error
        super().__init__(message)
    
    def __str__(self):
        msg = f"{self.message} (retry count: {self.retry_count})"
        if self.last_error:
            msg += f", last error: {str(self.last_error)}"
        return msg


class ValidationError(AgoraAPIError):
    """Parameter validation failure exception"""
    pass


class TimeoutError(AgoraAPIError):
    """Request timeout exception"""
    pass

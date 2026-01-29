"""
Base response models for Agora Conversational AI API

Corresponds to Go version: agora-rest-client-go/services/convoai/resp/base.go
"""
from typing import Optional
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """
    Base HTTP response
    
    Contains raw HTTP response information
    """
    http_status_code: int = Field(..., description="HTTP status code")
    raw_body: str = Field(..., description="Raw response body")
    
    class Config:
        arbitrary_types_allowed = True


class ErrResponse(BaseModel):
    """
    Error response returned by the Conversational AI engine API
    
    @since v0.7.0
    """
    detail: Optional[str] = Field(None, description="Error details")
    reason: Optional[str] = Field(None, description="Reason for the error")


class Response(BaseModel):
    """
    Response returned by the Conversational AI engine API
    
    @since v0.7.0
    """
    base_response: Optional[BaseResponse] = Field(None, description="HTTP base response")
    err_response: Optional[ErrResponse] = Field(default_factory=ErrResponse, description="Error response")
    
    def is_success(self) -> bool:
        """
        Determines whether the response returned by the Conversational AI engine API is successful
        
        Note: If the response is successful, continue to read the data in the successful response;
              otherwise, read the data in the error response
        
        Returns:
            True if successful (HTTP 200), otherwise False
        
        @since v0.7.0
        """
        if self.base_response is not None:
            return self.base_response.http_status_code == 200
        return False
    
    class Config:
        arbitrary_types_allowed = True

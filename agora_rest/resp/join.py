"""
Join API response models

Corresponds to Go version: agora-rest-client-go/services/convoai/resp/join.go
"""
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

from .base import BaseResponse, ErrResponse, Response


class JoinSuccessResp(BaseModel):
    """
    Successful response returned by the Conversational AI engine Join API
    
    @since v0.7.0
    """
    agent_id: str = Field(..., description="Unique identifier of the agent")
    create_ts: int = Field(..., description="Timestamp when the agent was created")
    status: str = Field(..., description="""Running status of the agent:
        - IDLE (0): The agent is idle
        - STARTING (1): The agent is starting
        - RUNNING (2): The agent is running
        - STOPPING (3): The agent is stopping
        - STOPPED (4): The agent has stopped
        - RECOVERING (5): The agent is recovering
        - FAILED (6): The agent has failed
    """)


class JoinResp(Response):
    """
    JoinResp returned by the Conversational AI engine Join API
    
    @since v0.7.0
    """
    success_resp: Optional[JoinSuccessResp] = Field(None, description="Successful response")
    
    @classmethod
    def from_http_response(
        cls,
        status_code: int,
        body: str,
        parsed_body: Optional[Dict[str, Any]] = None
    ) -> "JoinResp":
        """
        Create JoinResp from HTTP response
        
        Args:
            status_code: HTTP status code
            body: Raw response body
            parsed_body: Parsed JSON body (optional)
        
        Returns:
            JoinResp instance
        """
        base_resp = BaseResponse(http_status_code=status_code, raw_body=body)
        
        if status_code == 200 and parsed_body:
            # Success response
            success_resp = JoinSuccessResp(**parsed_body)
            return cls(
                base_response=base_resp,
                success_resp=success_resp
            )
        elif parsed_body:
            # Error response
            err_resp = ErrResponse(**parsed_body)
            return cls(
                base_response=base_resp,
                err_response=err_resp
            )
        else:
            # Unknown response
            return cls(base_response=base_resp)

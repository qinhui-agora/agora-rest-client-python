"""
Leave API response models

Corresponds to Go version: agora-rest-client-go/services/convoai/resp/leave.go
"""
from typing import Optional, Any, Dict
from pydantic import Field

from .base import BaseResponse, ErrResponse, Response


class LeaveResp(Response):
    """
    LeaveResp returned by the Conversational AI engine Leave API
    
    @since v0.7.0
    """
    
    @classmethod
    def from_http_response(
        cls,
        status_code: int,
        body: str,
        parsed_body: Optional[Dict[str, Any]] = None
    ) -> "LeaveResp":
        """
        Create LeaveResp from HTTP response
        
        Args:
            status_code: HTTP status code
            body: Raw response body
            parsed_body: Parsed JSON body (optional)
        
        Returns:
            LeaveResp instance
        """
        base_resp = BaseResponse(http_status_code=status_code, raw_body=body)
        
        if status_code == 200:
            # Success response (Leave API typically returns empty body on success)
            return cls(base_response=base_resp)
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

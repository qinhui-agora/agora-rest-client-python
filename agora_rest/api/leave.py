"""
Leave API handler

Corresponds to Go version: agora-rest-client-go/services/convoai/api/leave.go
"""
import logging

from ..config import Config
from ..resp.leave import LeaveResp
from .base_handler import BaseHandler


class LeaveAPI(BaseHandler):
    """
    Leave API handler
    
    Stops the specified agent instance and leaves the RTC channel
    """
    
    def __init__(
        self,
        module: str,
        logger: logging.Logger,
        retry_count: int,
        config: Config,
        prefix_path: str
    ):
        """
        Initialize Leave API handler
        
        Args:
            module: Module name for logging (e.g., "convoai:leave")
            logger: Logger instance
            retry_count: Number of retry attempts
            config: Configuration instance
            prefix_path: API path prefix
        """
        super().__init__(module, logger, retry_count, config, prefix_path)
    
    def build_path(self, agent_id: str) -> str:
        """
        Build request path
        
        Returns the request path:
        /api/conversational-ai-agent/v2/projects/{appid}/agents/{agentId}/leave
        
        Args:
            agent_id: Agent ID
        
        Returns:
            Request path
        """
        return f"{self.prefix_path}/agents/{agent_id}/leave"
    
    def do(self, agent_id: str) -> LeaveResp:
        """
        Execute Leave API request
        
        Args:
            agent_id: Agent ID to stop
        
        Returns:
            LeaveResp indicating success or failure
        
        Raises:
            AgoraAPIError: If request fails
            RetryError: If all retry attempts fail
        """
        path = self.build_path(agent_id)
        
        # Execute request with retry (POST with empty body)
        base_response = self.do_rest_with_retry(path, "POST", None)
        
        # Parse response
        status_code, raw_body, parsed_json = self.parse_response(base_response)
        
        # Create LeaveResp
        leave_resp = LeaveResp.from_http_response(
            status_code=status_code,
            body=raw_body,
            parsed_body=parsed_json
        )
        
        return leave_resp

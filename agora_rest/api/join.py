"""
Join API handler

Corresponds to Go version: agora-rest-client-go/services/convoai/api/join.go
"""
import logging
from typing import Optional

from ..config import Config
from ..req.join import JoinPropertiesReqBody
from ..resp.join import JoinResp
from .base_handler import BaseHandler


class JoinAPI(BaseHandler):
    """
    Join API handler
    
    Creates an agent instance and joins the specified RTC channel
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
        Initialize Join API handler
        
        Args:
            module: Module name for logging (e.g., "convoai:join")
            logger: Logger instance
            retry_count: Number of retry attempts
            config: Configuration instance
            prefix_path: API path prefix
        """
        super().__init__(module, logger, retry_count, config, prefix_path)
    
    def build_path(self) -> str:
        """
        Build request path
        
        Returns the request path:
        /api/conversational-ai-agent/v2/projects/{appid}/join
        
        Returns:
            Request path
        """
        return f"{self.prefix_path}/join"
    
    def do(
        self,
        name: str,
        properties_body: JoinPropertiesReqBody
    ) -> JoinResp:
        """
        Execute Join API request
        
        Args:
            name: Unique identifier for the agent (cannot be reused)
            properties_body: Configuration properties of the agent
        
        Returns:
            JoinResp containing agent_id, create_ts, and status
        
        Raises:
            AgoraAPIError: If request fails
            RetryError: If all retry attempts fail
        """
        path = self.build_path()
        
        # Build request body
        request = {
            "name": name,
            "properties": properties_body.dict(exclude_none=True, by_alias=True)
        }
        
        # Execute request with retry
        base_response = self.do_rest_with_retry(path, "POST", request)
        
        # Parse response
        status_code, raw_body, parsed_json = self.parse_response(base_response)
        
        # Create JoinResp
        join_resp = JoinResp.from_http_response(
            status_code=status_code,
            body=raw_body,
            parsed_body=parsed_json
        )
        
        return join_resp

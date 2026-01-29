"""
Base API handler with retry logic

Corresponds to Go version: agora-rest-client-go/services/convoai/api/basehandler.go and common.go
"""
import time
import json
import logging
from typing import Optional, Dict, Any, Tuple
import requests

from ..config import Config
from ..exceptions import AgoraAPIError, RetryError, TimeoutError as AgoraTimeoutError
from ..resp.base import BaseResponse


class BaseHandler:
    """
    Base handler for API requests
    
    Provides common functionality for all API handlers including:
    - HTTP request execution
    - Retry logic
    - Error handling
    - Logging
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
        Initialize base handler
        
        Args:
            module: Module name for logging (e.g., "convoai:join")
            logger: Logger instance
            retry_count: Number of retry attempts
            config: Configuration instance
            prefix_path: API path prefix (e.g., "/api/conversational-ai-agent/v2/projects/{appid}")
        """
        self.module = module
        self.logger = logger
        self.retry_count = retry_count
        self.config = config
        self.prefix_path = prefix_path
        
        # Create HTTP session with authentication
        self.session = requests.Session()
        auth_headers = config.credential.get_auth_header()
        self.session.headers.update(auth_headers)
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8"
        })
    
    def do_rest_with_retry(
        self,
        path: str,
        method: str,
        request_body: Optional[Any] = None
    ) -> BaseResponse:
        """
        Execute REST request with retry logic
        
        Corresponds to Go version: doRESTWithRetry in common.go
        
        Retry logic:
        - HTTP 200/201: Success, no retry
        - HTTP 4xx: Client error, no retry
        - HTTP 5xx or other errors: Retry with exponential backoff
        
        Args:
            path: API path (relative to base URL)
            method: HTTP method (GET, POST, etc.)
            request_body: Request body (will be JSON serialized)
        
        Returns:
            BaseResponse containing status code and raw body
        
        Raises:
            RetryError: If all retry attempts fail
            AgoraAPIError: If request fails with 4xx error
            AgoraTimeoutError: If request times out
        """
        base_url = self.config.get_base_url()
        full_url = f"{base_url}{path}"
        
        last_error: Optional[Exception] = None
        current_retry = 0
        
        while current_retry <= self.retry_count:
            try:
                # Execute HTTP request
                self.logger.debug(
                    f"[{self.module}] Sending {method} request to {full_url} "
                    f"(attempt {current_retry + 1}/{self.retry_count + 1})"
                )
                
                response = self._execute_request(full_url, method, request_body)
                status_code = response.status_code
                raw_body = response.text
                
                # Check status code
                if status_code in (200, 201):
                    # Success
                    self.logger.debug(
                        f"[{self.module}] Request successful: status={status_code}"
                    )
                    return BaseResponse(
                        http_status_code=status_code,
                        raw_body=raw_body
                    )
                elif 400 <= status_code < 500:
                    # Client error - no retry
                    self.logger.debug(
                        f"[{self.module}] Client error (no retry): "
                        f"status={status_code}, body={raw_body}"
                    )
                    raise AgoraAPIError(
                        f"HTTP {status_code}: {raw_body}",
                        status_code=status_code,
                        response_body=raw_body
                    )
                else:
                    # Server error or other - retry
                    self.logger.debug(
                        f"[{self.module}] Server error (will retry): "
                        f"status={status_code}, body={raw_body}"
                    )
                    last_error = AgoraAPIError(
                        f"HTTP {status_code}: {raw_body}",
                        status_code=status_code,
                        response_body=raw_body
                    )
                    
            except requests.exceptions.Timeout as e:
                self.logger.debug(f"[{self.module}] Request timeout: {str(e)}")
                last_error = AgoraTimeoutError(
                    f"Request timeout after {self.config.http_timeout}s"
                )
                
            except requests.exceptions.RequestException as e:
                self.logger.debug(f"[{self.module}] Request error: {str(e)}")
                last_error = AgoraAPIError(f"Request failed: {str(e)}")
            
            # Retry with exponential backoff
            if current_retry < self.retry_count:
                wait_time = current_retry + 1  # 1s, 2s, 3s, ...
                self.logger.debug(
                    f"[{self.module}] Retrying in {wait_time}s "
                    f"(attempt {current_retry + 1}/{self.retry_count})"
                )
                time.sleep(wait_time)
            
            current_retry += 1
        
        # All retries exhausted
        raise RetryError(
            f"Request failed after {self.retry_count + 1} attempts",
            retry_count=self.retry_count + 1,
            last_error=last_error
        )
    
    def _execute_request(
        self,
        url: str,
        method: str,
        request_body: Optional[Any]
    ) -> requests.Response:
        """
        Execute HTTP request
        
        Args:
            url: Full URL
            method: HTTP method
            request_body: Request body
        
        Returns:
            requests.Response object
        """
        # Serialize request body if present
        json_body = None
        if request_body is not None:
            if hasattr(request_body, 'dict'):
                # Pydantic model
                json_body = request_body.dict(exclude_none=True, by_alias=True)
            elif isinstance(request_body, dict):
                json_body = request_body
            else:
                json_body = request_body
        
        # Execute request
        if method.upper() == "GET":
            response = self.session.get(
                url,
                timeout=self.config.http_timeout
            )
        elif method.upper() == "POST":
            response = self.session.post(
                url,
                json=json_body,
                timeout=self.config.http_timeout
            )
        elif method.upper() == "PUT":
            response = self.session.put(
                url,
                json=json_body,
                timeout=self.config.http_timeout
            )
        elif method.upper() == "DELETE":
            response = self.session.delete(
                url,
                timeout=self.config.http_timeout
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    
    def parse_response(self, base_response: BaseResponse) -> Tuple[int, str, Optional[Dict[str, Any]]]:
        """
        Parse base response into components
        
        Args:
            base_response: BaseResponse object
        
        Returns:
            Tuple of (status_code, raw_body, parsed_json)
        """
        status_code = base_response.http_status_code
        raw_body = base_response.raw_body
        
        # Try to parse JSON
        parsed_json = None
        if raw_body:
            try:
                parsed_json = json.loads(raw_body)
            except json.JSONDecodeError:
                self.logger.warning(
                    f"[{self.module}] Failed to parse response as JSON: {raw_body}"
                )
        
        return status_code, raw_body, parsed_json

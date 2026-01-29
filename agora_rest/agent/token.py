"""
Token Builder

Utility for generating Agora tokens with RTC, RTM and Chat privileges.
"""
from ..utils import AccessToken, ServiceRtc, ServiceRtm, ServiceChat


class TokenBuilder:
    """Token generation utility"""
    
    @staticmethod
    def generate(
        app_id: str,
        app_certificate: str,
        channel_name: str,
        uid: str,
        expire: int = 86400
    ) -> str:
        """
        Generate Agora token with RTC, RTM and Chat privileges
        
        Args:
            app_id: Agora App ID
            app_certificate: Agora App Certificate
            channel_name: Channel name
            uid: User ID (string or integer)
            expire: Token expiration time in seconds (default 24 hours)
            
        Returns:
            Token string with RTC, RTM and Chat privileges
        """
        # Create RTC service
        rtc_service = ServiceRtc(channel_name, uid)
        rtc_service.add_privilege(ServiceRtc.kPrivilegeJoinChannel, expire)
        
        # Create RTM service
        rtm_service = ServiceRtm(uid)
        rtm_service.add_privilege(ServiceRtm.kPrivilegeLogin, expire)
        
        # Create Chat service
        chat_service = ServiceChat(uid)
        chat_service.add_privilege(ServiceChat.kPrivilegeUser, expire)
        
        # Create token and add all services
        token = AccessToken(app_id=app_id, app_certificate=app_certificate, expire=expire)
        token.add_service(rtc_service)
        token.add_service(rtm_service)
        token.add_service(chat_service)
        
        return token.build()

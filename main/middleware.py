from django.utils import timezone
from .models import Session
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

class CustomSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_token = request.COOKIES.get('sessionId')

        if not session_token:
            return None

        try:
            session = Session.objects.get(session_token=session_token)
            
            if session.expires_at <= timezone.now():
                session.delete()
                raise AuthenticationFailed('Session expired')

            if session.customer.account_status != 'Active':
                raise AuthenticationFailed('Account is not active Contact Admin')

            return (session.customer, session)

        except Session.DoesNotExist:
            raise AuthenticationFailed('Invalid session token')
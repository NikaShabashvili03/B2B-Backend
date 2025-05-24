from rest_framework import generics, status
from rest_framework.response import Response
from ..permissions import AllowAny, IsAuthenticated
from ..serializers.customer import CustomerSerializer, CustomerLoginSerializer
from django.middleware.csrf import get_token
import uuid
from django.utils.timezone import now
from datetime import timedelta
from ..models import Session

class LoginView(generics.GenericAPIView):
    serializer_class = CustomerLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csrf_token = get_token(request)

        customer = serializer.validated_data

        token = str(uuid.uuid4())
        customer.last_login = now()
        customer.save()

        expires_at = now() + timedelta(days=2)

        session = Session.objects.create(
            customer=customer,
            session_token=token,
            expires_at=expires_at,
        )

        customer_data = CustomerSerializer(customer).data

        response = Response(customer_data, status=status.HTTP_200_OK)
        response.set_cookie(
            'sessionId', session.session_token, expires=expires_at, 
            samesite='None', secure=True
        )
        csrf_token = get_token(request)
        response['X-CSRFToken'] = csrf_token
        return response
    


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    
    def get(self, request, *args, **kwargs):
        customer = request.user
        serializer = CustomerSerializer(customer, context={'request': request})

        return Response(serializer.data)
    

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        customer = request.user
        sessions = Session.objects.filter(customer_id=customer).distinct()
        response = Response({'details': 'Logged out successfully'}, status=status.HTTP_200_OK)
        if sessions:
            sessions.delete()
            response.delete_cookie('sessionId')
        else:
            response = Response({'details': 'Invalid session token'}, status=status.HTTP_400_BAD_REQUEST)
            
        return response
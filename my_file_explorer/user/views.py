from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, MyTokenObtainPairSerializer


User = get_user_model()


def get_tokens_for_user(user):
    refresh = MyTokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUpUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LogoutView(APIView):
    """Logout view that removes jwt token from cookies"""

    @swagger_auto_schema(tags=["user"])
    def post(self, request):
        # Blacklist refresh token
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['REFRESH_COOKIE'], '')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        # Delete cookies
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        response.data = {"Success": "Logout successfully"}
        return response


class ManageUserView(generics.RetrieveAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

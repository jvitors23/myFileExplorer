from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from user.serializers import LoginSerializer, UserSerializer


User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoginView(APIView):

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer, tags=["user"])
    def post(self, request):
        """Login view that saves JWT token using browser cookies"""
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        if not user.is_active:
            raise AuthenticationFailed("User is not active!")

        data = get_tokens_for_user(user)
        response = Response()
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value=data["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        csrf.get_token(request)
        response.data = {"Success": "Login successfully", "data": data}
        return response


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

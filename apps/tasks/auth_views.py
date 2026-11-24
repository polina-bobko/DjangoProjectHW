from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    AccessToken,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)

from drf_yasg.utils import swagger_auto_schema

from apps.core.jwt_cookies import (
    set_jwt_cookies,
    delete_jwt_cookies,
)
from .serializers import RegisterSerializer


User = get_user_model()

@method_decorator(csrf_protect, name="dispatch")
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class CsrfTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({
            "csrfToken": get_token(request)
        })

@method_decorator(csrf_protect, name="dispatch")
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(
            request, *args, **kwargs
        )

        if response.status_code == status.HTTP_200_OK:
            set_jwt_cookies(
                response,
                access=response.data["access"],
                refresh=response.data["refresh"],
            )

            response.data = {
                "message": "Login successful."
            }

        return response

@method_decorator(csrf_protect, name="dispatch")
class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")

        if not refresh:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data={"refresh": refresh}
        )

        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data

        response = Response(
            {"message": "Tokens refreshed successfully."},
            status=status.HTTP_200_OK,
        )

        return set_jwt_cookies(
            response,
            access=tokens["access"],
            refresh=tokens.get("refresh", refresh),
        )

@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            204: "Successfully logged out.",
        }
    )
    def post(self, request, *args, **kwargs):
        refresh_value = request.COOKIES.get(
            "refresh_token"
        )

        access_value = request.COOKIES.get(
            "access_token"
        )

        if refresh_value:
            try:
                refresh = RefreshToken(refresh_value)
                refresh.blacklist()
            except TokenError:
                pass

        if access_value:
            try:
                access = AccessToken(access_value)

                outstanding_token, _ = (
                    OutstandingToken.objects.get_or_create(
                        jti=access[api_settings.JTI_CLAIM],
                        defaults={
                            "token": str(access),
                            "created_at": datetime.fromtimestamp(
                                access["iat"],
                                tz=timezone.utc,
                            ),
                            "expires_at": datetime.fromtimestamp(
                                access["exp"],
                                tz=timezone.utc,
                            ),
                        },
                    )
                )

                BlacklistedToken.objects.get_or_create(
                    token=outstanding_token
                )

            except TokenError:
                pass

        response = Response(
            status=status.HTTP_204_NO_CONTENT
        )

        return delete_jwt_cookies(response)
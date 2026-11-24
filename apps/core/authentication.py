from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)

        if header is not None:
            return super().authenticate(request)

        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(
            raw_token
        )

        user = self.get_user(validated_token)

        SessionAuthentication().enforce_csrf(request)

        return user, validated_token

    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)

        if BlacklistedToken.objects.filter(
            token__jti=token[api_settings.JTI_CLAIM]
        ).exists():
            raise AuthenticationFailed(
                "Token has been revoked."
            )

        return token
from datetime import datetime, timezone

from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def set_jwt_cookies(response, access, refresh):
    tokens = {
        "access_token": AccessToken(access),
        "refresh_token": RefreshToken(refresh),
    }

    for name, token in tokens.items():
        response.set_cookie(
            key=name,
            value=str(token),
            expires=datetime.fromtimestamp(
                token["exp"],
                tz=timezone.utc,
            ),
            httponly=True,
            secure=settings.JWT_COOKIE_SECURE,
            samesite="Lax",
            path="/",
        )

    response["Cache-Control"] = "no-store"

    return response


def delete_jwt_cookies(response):
    response.delete_cookie(
        "access_token",
        path="/",
        samesite="Lax",
    )

    response.delete_cookie(
        "refresh_token",
        path="/",
        samesite="Lax",
    )

    response["Cache-Control"] = "no-store"

    return response
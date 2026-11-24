from django.urls import path

from .auth_views import (
    RegisterView,
    LoginView,
    RefreshView,
    LogoutView,
    CsrfTokenView,
)

urlpatterns = [
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register-view",
    ),
    path(
        "auth/login/",
        LoginView.as_view(),
        name="token-obtain-pair-view",
    ),
    path(
        "auth/refresh/",
        RefreshView.as_view(),
        name="token-refresh-view",
    ),
    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout-view",
    ),
    path(
        "auth/csrf/",
        CsrfTokenView.as_view(),
        name="csrf-token-view",
    ),
]
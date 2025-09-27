# auth_api/urls.py
from django.urls import path, include
from .views import RegisterView,  LoginView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # DRF’s built-in login/logout/password endpoints (session-based auth)
    path("", include("rest_framework.urls")),
]


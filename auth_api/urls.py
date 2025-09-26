# auth_api/urls.py
from django.urls import path, include
from .views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    # DRF’s built-in login/logout/password endpoints (session-based auth)
    path("", include("rest_framework.urls")),
]


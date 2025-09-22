# auth_api/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserRegisterSerializer, CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Register a new user",
        request=UserRegisterSerializer,
        responses={
            201: OpenApiExample(
                "Successful Registration",
                value={
                    "message": "User registered successfully",
                    "user": {
                        "id": 1,
                        "username": "new_user",
                        "email": "new_user@example.com"
                    }
                },
            ),
            400: OpenApiExample(
                "Validation Error",
                value={"username": ["This field is required."]},
            ),
        },
    )
)
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Obtain JWT token pair (Login)",
        request=CustomTokenObtainPairSerializer,
        responses={
            200: OpenApiExample(
                "Login Success",
                value={
                    "refresh": "string.jwt.refresh.token",
                    "access": "string.jwt.access.token",
                },
            ),
            401: OpenApiExample(
                "Invalid credentials",
                value={"detail": "No active account found with the given credentials"},
            ),
        },
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Refresh access token",
        request={
            "refresh": "string.jwt.refresh.token",
        },
        responses={
            200: OpenApiExample(
                "Refresh Success",
                value={"access": "string.jwt.new.access.token"},
            ),
            401: OpenApiExample(
                "Invalid token",
                value={"detail": "Token is invalid or expired"},
            ),
        },
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

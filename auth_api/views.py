# auth_api/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from .serializers import UserRegisterSerializer


@extend_schema(
    summary="Register a new user",
    description="Creates a new user account. Requires username and password (and optionally email).",
    request=UserRegisterSerializer,
    responses={201: UserRegisterSerializer},
    examples=[
        OpenApiExample(
            "Registration Example",
            value={
                "username": "testuser",
                "password": "StrongPassword123",
                "email": "user@example.com"
            },
        )
    ],
    tags=["Auth"],
)
class RegisterView(generics.CreateAPIView):
    """
    A public endpoint that allows new users to register.
    No authentication or token is required since JWT has been removed.
    """
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


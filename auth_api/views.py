# auth_api/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from .serializers import UserRegisterSerializer


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


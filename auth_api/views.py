# auth_api/views.py
'''from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import UserRegisterSerializer
from django.contrib.auth import authenticate, login, logout
# -------------------------
# Register View
# -------------------------
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
                "password2": "StrongPassword123",
                "email": "user@example.com"
            },
        )
    ],
    tags=["Auth"],
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

# -------------------------
# Login View
# -------------------------
@extend_schema(
    summary="Login a user",
    description="Logs in a user using session authentication. Requires username and password.",
    examples=[
        OpenApiExample(
            "Login Example",
            value={
                "username": "testuser",
                "password": "StrongPassword123"
            },
        )
    ],
    tags=["Auth"],
)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"message": "Login successful"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

# -------------------------
# Logout View
# -------------------------
@extend_schema(
    summary="Logout a user",
    description="Logs out the currently authenticated user.",
    tags=["Auth"],
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK,
        )
'''

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})

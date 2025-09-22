from django.contrib.auth import get_user_model 
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend SimpleJWT's TokenObtainPairSerializer to include extra fields if needed.
    Right now, just return tokens and username.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom fields here (optional)
        data.update(
            {
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "email": self.user.email,
                }
            }
        )
        return data
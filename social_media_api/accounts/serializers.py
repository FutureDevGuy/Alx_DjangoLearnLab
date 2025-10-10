from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # ✅ Create user properly using Django's built-in method
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        # ✅ Create token for the new user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for logging in a user."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read/update)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

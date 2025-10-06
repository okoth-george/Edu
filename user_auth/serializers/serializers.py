from rest_framework import serializers
from user_auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate(self, data):
        # Additional validation logic can be added here if needed
        return data
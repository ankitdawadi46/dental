from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_tenants.utils import schema_context
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from dental_app.utils.response import BaseResponse
from users.queries import user_with_profile_exists


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, required=True)
    tenant_schema_name = serializers.CharField(required=True)

    def validate(self, data):
        """
        Custom validation logic to check if user already exists.
        """
        email = data.get("email")
        tenant_schema_name = data.get("tenant_schema_name")
        password = data.get("password")
        
        if not email or not password or not tenant_schema_name:
            raise BaseResponse(
                data={"error": "Email, password, and tenant schema name are required."},
                code=400,
            )

        # Validate if email already exists
        if user_with_profile_exists(email):
            raise ValidationError("A user with this email already exists.")

        # You can also add more validation checks for tenant_schema_name if needed.

        # Validate required fields


        # Validate password length
        if len(password) < 8:
            return BaseResponse(
                data={"error": "Password must be at least 8 characters long."},
                code=400,
            )

        return data
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

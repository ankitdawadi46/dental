from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django_tenants.utils import schema_context
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Profile
from utils.username_from_email import get_username_from_email


class SignupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    """
    A ViewSet implementation for user signup without using forms.
    """

    def create(self, request, *args, **kwargs):
        """
        Handles the POST request for signup.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        tenant_schema_name = request.data.get("tenant_schema_name")  # Ensure tenant schema name is provided
        username = get_username_from_email(email)

        # Validate required fields
        if not email or not password or not tenant_schema_name:
            return Response(
                {"error": "Email, password, and tenant schema name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate password length
        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Switch to the correct tenant schema
            with schema_context(tenant_schema_name):

                # Create user
                user = User.objects.create(
                    email=email,
                    password=make_password(password),  # Hash the password
                    username=username,
                )

                # Create user profile
                Profile.objects.create(user=user)

            return Response(
                {"message": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {"error": "A user with this username or email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Create your views here.
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    """
    A ViewSet implementation for user login
    """

    def create(self, request, *args, **kwargs):
        """
        Handles the POST request for login.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me", False)

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)

            # Handle session expiry based on "remember_me"
            if not remember_me:
                request.session.set_expiry(0)

            return Response(
                {"message": "Login successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid Username and/or Password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

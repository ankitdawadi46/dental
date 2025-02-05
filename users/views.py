import random
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from client.models import OTP, CustomUser, Profile
from dental_app.utils.exceptions import AuthenticationError
from dental_app.utils.response import BaseResponse
from users.selectors.factories.login_factory import LoginFactory
from users.selectors.factories.otp_email_factory import OTPEmailFactory
from users.selectors.factories.password_factory import DefaultPasswordFactory
from users.selectors.factories.signup_factory import SignUpFactory
from users.selectors.forget_password_service import ForgotPasswordService
from users.serializers import (
    ForgotPasswordSerializer,
    LogoutSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
)
from utils.generate_otp import generate_otp


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
        tenant_schema_name = request.data.get(
            "tenant_schema_name"
        )  # Ensure tenant schema name is provided

        # Validate required fields
        # if not email or not password or not tenant_schema_name:
        #     return Response(
        #         {"error": "Email, password, and tenant schema name are required."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        # # Validate password length
        # if len(password) < 8:
        #     return Response(
        #         {"error": "Password must be at least 8 characters long."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        try:
            # Switch to the correct tenant schema
            # Create user
            otp = str(random.randint(100000, 999999))
            user = CustomUser.objects.create(
                is_verified=False,
                otp=otp,
                email=email,
                password=make_password(password),  # Hash the password
            )

            # Create user profile
            Profile.objects.create(user=user)

            return Response(
                {"message": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Create your views here.
class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    """
    A ViewSet implementation for user login
    """

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        """
        Handles the POST request for login.
        """
        try:
            token = LoginFactory(request).login()
            return BaseResponse(data={"token": token}, status=200)
        except AuthenticationError as e:
            # Handle authentication errors and use the status code from the exception
            return BaseResponse(
                data={"error": str(e)}, status=e.code
            )  # Use the custom error code (e.g., 401)
        except Exception:
            # Handle other unforeseen errors
            return BaseResponse(
                data={"error": "An unexpected error occurred."}, status=400
            )

    @action(detail=False, methods=["post"])
    def signup(self, request, *args, **kwargs):
        """
        Handles the POST request for signup.
        """
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            signup_factory = SignUpFactory(serializer=serializer).signup()
            return signup_factory
        else:
            return BaseResponse(data={"errors": serializer.errors}, status=400)
        
    @action(detail=False, methods=["post"])
    def verify_otp(self, request, *args, **kwargs):
        """
        Handles the POST request to verify OTP.
        """
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            # Get user by email
            user = CustomUser.objects.get(email=email)
            otp_instance = OTP.objects.get(user=user, otp=otp, is_used=False, purpose="SignUp")

            # Check if OTP is expired
            if otp_instance.is_expired():
                return BaseResponse(
                    data={"error": "OTP has expired"},
                    status=400)
            user.is_verified = True
            user.save()
            otp_instance.is_used = True
            otp_instance.save()
            # OTP is valid and not expired
            return BaseResponse(
                data={"message": "OTP verified successfully"}, 
                status=200)

        except OTP.DoesNotExist:
            return BaseResponse(
                data={"error": "Invalid OTP"}, status=400)
        except CustomUser.DoesNotExist:
            return BaseResponse(
                data={"error": "User not found"}, status=404)
        
    @action(detail=False, methods=['POST'])
    def resent_otp(self, request):
        email = request.data.get("email")
        purpose = request.data.get("purpose")
        try:
            user = CustomUser.objects.get(email=email)
            otp_value = generate_otp(user, purpose)
            otp_email_factory = OTPEmailFactory()
            email_thread = otp_email_factory.create_email_thread_verification(user.email, otp_value)
            email_thread.start()
            return BaseResponse(
                data={"message": "OTP resend to your email."},
                status=200,
            )
            
        except CustomUser.DoesNotExist:
            return BaseResponse(data="USer not found!!!")
            
    @action(detail=False, methods=["post"])
    def forgot_password(self, request):
        """
        Handles the POST request to send password reset email.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            # Create the factory instance and get the service
            factory = DefaultPasswordFactory()
            forgot_password_service = factory.create_forgot_password_service()

            if forgot_password_service.send_otp_email(email):
                return Response(
                    {"message": "Password reset otp sent successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["POST"],
        url_path="reset-password",
    )
    def reset_password(self, request):
        """
        Handles the POST request to reset the password.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            confirm_password = serializer.validated_data["confirm_password"]
            otp = serializer.validated_data['otp']
            email = serializer.validated_data['email']

            # Create the factory instance and get the service
            try:
                otp = OTP.objects.get(otp=otp, purpose="ForgotPassword", user__email=email, is_used=False)
                if otp.is_expired():
                    return BaseResponse(
                        data="OTP is expired",
                        status=400
                    )
                    
                factory = DefaultPasswordFactory()
                reset_password_service = factory.create_reset_password_service()

                if reset_password_service.reset_password(
                    email, otp, new_password, confirm_password
                ):
                    otp.is_used = True
                    otp.save()
                    return BaseResponse(
                        data={"Password reset successfully."},
                        status=200,
                    )

                else:
                    return BaseResponse(
                        data={"Invalid token or passwords don't match."},
                        status=400
                    )
            except (OTP.DoesNotExist, ValueError):
                return BaseResponse(
                    data="Invalid OTP or email address",
                    status=400
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return BaseResponse(
                data={"Successfully logout"},
                status=204
            )
        else:
            return BaseResponse(data={"errors": serializer.errors}, status=400)
        

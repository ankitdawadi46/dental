from django.utils.crypto import get_random_string
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from client.models import Client, ClinicProfile, CustomUser, Domain, Profile
from users.selectors.user_creator import UserCreator


class DashboardSerializer(Serializer):
    pass


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class CustomUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "middle_name", "last_name", "password"]

    def create(self, validated_data):
        user_creator = UserCreator()
        password = get_random_string(10)
        user = user_creator.create_user(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            is_staff=False,
            is_superuser=False,
            password=password
        )
        return user
        

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "user",
            "photo",
            "dob",
            "gender",
            "profile_type",
            "designation",
            "address",
            "phone_number",
            "nmc_no",
            "nhpc_no",
        ]

class ProfileGetSerializer(ModelSerializer):
    user = CustomUserSerializer()
    
    class Meta:
        model = Profile
        fields = "__all__"


class ClinicProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicProfile
        fields = ['id', 'clinic', 'user']
        

class ClinicProfileGetSerializer(serializers.ModelSerializer):
    user = ProfileGetSerializer()
    
    class Meta:
        model = ClinicProfile
        fields = "__all__"

from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at", "author"]

    def create(self, validated_data):
        # Automatically set the author as the logged-in user
        request = self.context.get("request")
        # if request and hasattr(request, "user"):
        #     validated_data["author"] = request.user
        return super().create(validated_data)
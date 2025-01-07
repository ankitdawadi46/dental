from rest_framework.permissions import BasePermission

from client.models import Profile


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if  not request.user.is_staff:
            try:
                profile = Profile.objects.select_related("user").get(user=request.user)
                if profile.profile_type == "Doctor":
                    return True
            except Profile.DoesNotExist:
                return False
        return True
    

class IsIntern(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            try:
                profile = Profile.objects.select_related("user").get(user=request.user)
                if profile.profile_type == "Intern":
                    return True
            except Profile.DoesNotExist:
                return False
        return True
    

class IsHelper(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            try:
                profile = Profile.objects.select_related("user").get(user=request.user)
                if profile.profile_type == "Helper":
                    return True
            except Profile.DoesNotExist:
                return False
        return True
    

class IsClient(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            try:
                profile = Profile.objects.select_related("user").get(user=request.user)
                if profile.profile_type == "Client":
                    return True
            except Profile.DoesNotExist:
                return False
        return True
    

from rest_framework.routers import DefaultRouter

from users.views import SignupViewSet, UserViewSet

app_name = "user"

router = DefaultRouter()

router.register(r"sign-up", SignupViewSet, "signup")
router.register(r"user", UserViewSet, "user")

urlpatterns = [
    
]

urlpatterns = router.urls




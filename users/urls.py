from rest_framework.routers import DefaultRouter

from users.views import SignupViewSet, LoginViewSet

app_name = "user"

router = DefaultRouter()

router.register(r"sign-up", SignupViewSet, "signup")
router.register(r"login", LoginViewSet, "login")

urlpatterns = [
    
]

urlpatterns = router.urls




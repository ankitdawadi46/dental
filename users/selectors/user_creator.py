from django.contrib.auth import get_user_model

from users.domains import IUserCreator

User = get_user_model()


class UserCreator(IUserCreator):
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        is_superuser: bool = False,
        is_staff: bool = False
    ) -> User:
        user, _ = User.objects.get_or_create(
            username=email, email=email, firstname=first_name, lastname=last_name
        )
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.set_password(password)
        user.save()
        return user

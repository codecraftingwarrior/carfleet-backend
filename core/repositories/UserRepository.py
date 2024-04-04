from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository:

    @staticmethod
    def find_by_id(user_id) -> User:
        return User.objects.get(pk=user_id)

    @staticmethod
    def store_user(username: str, email: str, first_name: str, last_name: str, address: str, phone: str,
                   password: str) -> User:
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone
        )
        user.set_password(password)

        return user

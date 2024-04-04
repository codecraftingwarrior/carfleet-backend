from django.contrib.auth import get_user_model

from core import repositories, enums

User = get_user_model()


class ApplicationUserService:

    @staticmethod
    def _create_customer(username: str, email: str, first_name: str, last_name: str, address: str, phone: str,
                         password: str) -> User:
        customer_group = repositories.GroupRepository.get_customer_group()

        user = repositories.UserRepository.store_user(username, email, first_name, last_name, address, phone, password)

        customer_group.user_set.add(user)

        return user

    @staticmethod
    def _create_admin(username: str, email: str, first_name: str, last_name: str, address: str, phone: str,
                      password: str) -> User:
        admin_group = repositories.GroupRepository.get_admin_group()

        user = repositories.UserRepository.store_user(username, email, first_name, last_name, address, phone, password)

        admin_group.user_set.add(user)

        return user

    @staticmethod
    def create_user(role: enums.BasicRole, username: str, email: str, first_name: str, last_name: str, address: str,
                    phone: str,
                    password: str) -> User:
        if role == enums.BasicRole.ADMIN:
            return ApplicationUserService._create_admin(
                username,
                email,
                first_name,
                last_name,
                address,
                phone,
                password
            )
        elif role == enums.BasicRole.CUSTOMER:
            return ApplicationUserService._create_customer(
                username,
                email,
                first_name,
                last_name,
                address,
                phone,
                password
            )

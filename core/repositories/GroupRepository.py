from django.contrib.auth.models import Group


class GroupRepository:

    @staticmethod
    def find_by_name(name: str) -> Group:
        return Group.objects.get(name=name)

    @staticmethod
    def get_admin_group() -> Group:
        group, _ = Group.objects.get_or_create(name='Admin')
        return group

    @staticmethod
    def get_customer_group() -> Group:
        group, _ = Group.objects.get_or_create(name='Customer')
        return group

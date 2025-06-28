from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=input("Введите email\n"),
        )

        user.set_password(input("Введите пароль\n"))
        user.save()

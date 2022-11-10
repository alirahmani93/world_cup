import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from common.models import Configuration
from user.models import User


class Command(BaseCommand):
    help = 'This command setup project'

    def handle(self, *args, **options):
        self.create_configuration()
        self.create_super_user()
        self.create_system_user()

    def create_configuration(self):
        try:
            Configuration.objects.get_or_create()

            if sys.argv[1] != 'test':
                self.stdout.write(self.style.SUCCESS('Successfully Create Configuration\n'))
        except Exception as e:
            print(e)
            self.stdout.write(self.style.WARNING('Exception has been occur'))
            raise CommandError('Error in Generating')

    def create_super_user(self):
        try:
            admin, is_created = User.objects.get_or_create(
                username=settings.ROOT_USER_NAME,
                mobile_number=settings.ROOT_USER_MOBILE_NUMBER,
                email=settings.ROOT_USER_EMAIL,
                is_staff=True, is_superuser=True
            )
            if is_created:
                admin.set_password(settings.ROOT_USER_PASSWORD)
                admin.save()
                print('super user created')
            else:
                print('super user already exists')
        except Exception as e:
            self.stdout.write(self.style.WARNING(e))

    def create_system_user(self):
        try:
            system, is_created = User.objects.get_or_create(
                username=settings.SYSTEM_USER_NAME,
                mobile_number=settings.SYSTEM_USER_MOBILE_NUMBER,
                email=settings.SYSTEM_USER_EMAIL,
                is_staff=True, is_superuser=True
            )
            if is_created:
                system.set_password(settings.SYSTEM_USER_PASSWORD)
                system.save()
                print('system user created')
            else:
                print('system user already exists')
        except Exception as e:
            self.stdout.write(self.style.WARNING(e))

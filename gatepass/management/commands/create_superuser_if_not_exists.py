"""
Django management command to create a superuser if one doesn't exist.
Can be used with environment variables for automated deployment.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist. Can use environment variables.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the superuser',
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the superuser',
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hostel.com'),
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser',
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123'),
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Do not prompt for input (use environment variables)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        noinput = options['noinput']

        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists. Skipping creation.')
            )
            return

        # Check if any superuser exists (by checking is_superuser or role='superadmin')
        if User.objects.filter(role='superadmin').exists():
            self.stdout.write(
                self.style.WARNING('A superuser already exists. Skipping creation.')
            )
            return

        # Create superuser
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='superadmin',
                is_staff=True,
                is_superuser=True,
                is_approved=True,  # Auto-approve superuser
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with email "{email}"'
                )
            )
            if not noinput:
                self.stdout.write(
                    self.style.WARNING(
                        'Please change the default password after first login!'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )


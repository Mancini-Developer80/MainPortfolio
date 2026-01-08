from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser on Render using credentials you provide'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--noinput', action='store_true', help='No interactive prompts')

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists!'))
            existing = User.objects.filter(is_superuser=True).first()
            self.stdout.write(f'Existing superuser: {existing.username} ({existing.email})')
            return

        if options['noinput']:
            username = options.get('username', 'admin')
            email = options.get('email', 'admin@example.com')
            password = options.get('password')
            
            if not password:
                self.stdout.write(self.style.ERROR('Password required with --noinput'))
                return
        else:
            self.stdout.write(self.style.SUCCESS('=== Create Superuser ==='))
            username = input('Username: ') or 'admin'
            email = input('Email: ') or 'admin@example.com'
            password = getpass.getpass('Password: ')
            password_confirm = getpass.getpass('Confirm password: ')
            
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Passwords do not match!'))
                return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Superuser "{username}" created successfully!'))

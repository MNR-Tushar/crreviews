from django.core.management.base import BaseCommand
from userprofile.models import User
from cr.models import University, Department
import os

class Command(BaseCommand):
    help = 'Create admin superuser from environment variables'

    def handle(self, *args, **kwargs):
        # Get credentials from environment variables
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PASSWORD')
        first_name = os.getenv('ADMIN_FIRST_NAME', 'Admin')
        last_name = os.getenv('ADMIN_LAST_NAME', 'User')
        
        # Validation
        if not email or not password:
            self.stdout.write(
                self.style.WARNING('⚠️  ADMIN_EMAIL and ADMIN_PASSWORD not set in environment variables')
            )
            self.stdout.write(
                self.style.WARNING('Superuser creation skipped.')
            )
            return

        # Check if superuser already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'✓ Superuser with email {email} already exists')
            )
            return

        try:
            # Create superuser
            admin_user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                gender='M',  # Default gender
                is_staff=True,
                is_active=True,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Email: {email}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Name: {first_name} {last_name}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )
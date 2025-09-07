import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likhoncombd.settings')
django.setup()

from django.contrib.auth.models import User

username = 'Gemini'
email = 'google@google.com'
password = 'gemini'
first_name = 'Google'

# Check if the user already exists
if not User.objects.filter(username=username).exists():
    # Create the user
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name
    )
    print(f"User '{username}' created successfully.")
else:
    print(f"User '{username}' already exists.")
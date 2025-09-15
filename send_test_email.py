
from django.core.mail import send_mail
from django.conf import settings

def send_test_email():
    try:
        send_mail(
            'Test Email from Django',
            'This is a test email sent from your Django application.',
            settings.DEFAULT_FROM_EMAIL,
            ['likhonsorkar002@gmail.com'],
            fail_silently=False,
        )
        print('Test email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likhoncombd.settings')
    django.setup()
    send_test_email()

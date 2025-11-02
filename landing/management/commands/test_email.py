from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email sending functionality'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address to send test email to')

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write('Testing email configuration...')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write('')
        
        try:
            self.stdout.write(f'Sending test email to {test_email}...')
            
            msg = EmailMultiAlternatives(
                subject='Test Email from Aigis',
                body='This is a test email from Aigis. If you receive this, email is working!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_email],
            )
            msg.send(fail_silently=False)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Test email sent successfully to {test_email}'))
            self.stdout.write('Check your inbox (and spam folder) for the test email.')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to send email: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
            self.stdout.write('')
            self.stdout.write('Common issues:')
            self.stdout.write('1. Gmail App Password might be incorrect - regenerate at https://myaccount.google.com/apppasswords')
            self.stdout.write('2. 2-Factor Authentication must be enabled on your Google account')
            self.stdout.write('3. Check if Gmail is blocking less secure apps (unlikely with app passwords)')
            self.stdout.write('4. Try using console backend: EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"')


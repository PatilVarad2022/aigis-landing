from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from landing.models import UserProfile

class Command(BaseCommand):
    help = 'Send welcome emails to users who signed up but haven\'t received emails yet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Send email to a specific user by email address',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Send emails to all users (use with caution)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Limit number of emails to send (default: 10)',
        )

    def handle(self, *args, **options):
        if options['email']:
            # Send to specific user
            try:
                user = User.objects.get(email=options['email'].lower())
                self.send_welcome_email(user)
                self.stdout.write(self.style.SUCCESS(f'✓ Welcome email sent to {user.email}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email {options["email"]} not found.'))
        elif options['all']:
            # Send to all users (with limit)
            users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:options['limit']]
            count = 0
            for user in users:
                try:
                    self.send_welcome_email(user)
                    count += 1
                    self.stdout.write(f'✓ Sent to {user.email}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed to send to {user.email}: {e}'))
            self.stdout.write(self.style.SUCCESS(f'\n✓ Sent {count} welcome emails'))
        else:
            self.stdout.write(self.style.WARNING(
                'Please specify --email <email> or --all to send emails.\n'
                'Example: python manage.py send_welcome_emails --email user@example.com'
            ))

    def send_welcome_email(self, user):
        """Send welcome email to a user"""
        try:
            profile = user.profile
            full_name = profile.full_name
            shield = profile.shield_limit_percent
        except UserProfile.DoesNotExist:
            full_name = user.email.split('@')[0]
            shield = 10
        
        # HTML email content
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Aigis</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; line-height: 1.6;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8fafc; padding: 40px 0;">
        <tr>
            <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.1); overflow: hidden;">
                    <tr>
                        <td style="background: linear-gradient(135deg, #0067FF 0%, #00FF8C 100%); padding: 40px 40px 50px; text-align: center;">
                            <div style="font-size: 36px; font-weight: bold; color: #ffffff; margin-bottom: 12px;">🛡️</div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">Welcome to Aigis!</h1>
                            <p style="margin: 12px 0 0; color: rgba(255, 255, 255, 0.95); font-size: 16px;">Your AI Trading Partner is Ready</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 24px; color: #0f172a; font-size: 18px; font-weight: 600;">Hi {full_name},</p>
                            <p style="margin: 0 0 24px; color: #475569; font-size: 16px;">
                                Welcome to Aigis! We're <strong style="color: #0067FF;">thrilled</strong> to have you join us.
                            </p>
                            <div style="background: linear-gradient(135deg, rgba(0, 255, 140, 0.1) 0%, rgba(0, 103, 255, 0.1) 100%); border-left: 4px solid #00FF8C; padding: 20px; border-radius: 8px; margin: 32px 0;">
                                <p style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 700; margin-bottom: 8px;">🎉 Your 28-Day Free Trial is Now Active</p>
                                <p style="margin: 0; color: #64748b; font-size: 15px;">Loss Shield: {shield}%</p>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''
        
        text_content = f'''Hi {full_name},

Welcome to Aigis! We're thrilled to have you join us.

🎉 Your 28-Day Free Trial is Now Active

Loss Shield: {shield}%

Ready to trade smarter? Let's do this together.

— The Aigis Team'''
        
        # Send email
        msg = EmailMultiAlternatives(
            subject='Welcome to Aigis! 🛡️ Your AI Trading Partner is Ready',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)


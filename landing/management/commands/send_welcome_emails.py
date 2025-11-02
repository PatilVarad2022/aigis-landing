from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from landing.models import UserProfile, PendingEmail

class Command(BaseCommand):
    help = 'Process queued emails and send them automatically (runs every few minutes)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Maximum number of emails to process (default: 20)',
        )
        parser.add_argument(
            '--delay-minutes',
            type=int,
            default=2,
            help='Only process emails older than X minutes (default: 2)',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        delay_minutes = options['delay_minutes']
        
        # Get pending emails that are old enough and not sent yet
        cutoff_time = timezone.now() - timedelta(minutes=delay_minutes)
        pending_emails = PendingEmail.objects.filter(
            sent=False,
            created_at__lte=cutoff_time
        ).order_by('created_at')[:limit]
        
        total = pending_emails.count()
        if total == 0:
            self.stdout.write('No pending emails to send.')
            return
        
        self.stdout.write(f'Processing {total} pending email(s)...')
        
        sent_count = 0
        failed_count = 0
        
        for pending_email in pending_emails:
            try:
                if pending_email.email_type == 'welcome':
                    self.send_welcome_email_from_queue(pending_email)
                elif pending_email.email_type == 'admin_notification':
                    self.send_admin_notification_from_queue(pending_email)
                
                # Mark as sent
                pending_email.sent = True
                pending_email.sent_at = timezone.now()
                pending_email.save()
                
                sent_count += 1
                self.stdout.write(f'✓ Sent {pending_email.email_type} email to {pending_email.email_data.get("to", "unknown")}')
                
            except Exception as e:
                pending_email.attempts += 1
                pending_email.save()
                failed_count += 1
                self.stdout.write(self.style.ERROR(f'✗ Failed to send {pending_email.email_type} email: {e}'))
                # Don't mark as sent if it failed - will retry next run
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Processed {total} emails: {sent_count} sent, {failed_count} failed'
        ))

    def send_welcome_email_from_queue(self, pending_email):
        """Send welcome email from queued data"""
        email_data = pending_email.email_data
        
        msg = EmailMultiAlternatives(
            subject=email_data['subject'],
            body=email_data['text_content'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_data['to']],
        )
        msg.attach_alternative(email_data['html_content'], "text/html")
        msg.send(fail_silently=False)
    
    def send_admin_notification_from_queue(self, pending_email):
        """Send admin notification from queued data"""
        email_data = pending_email.email_data
        
        send_mail(
            subject=email_data['subject'],
            message=email_data['message'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_data['to']],
            fail_silently=False,
        )


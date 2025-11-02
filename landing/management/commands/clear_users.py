from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from landing.models import UserProfile

class Command(BaseCommand):
    help = 'Clear all user data (emails, profiles) from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion (required to actually delete)',
        )

    def handle(self, *args, **options):
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
        self.stdout.write(f'Found {user_count} users and {profile_count} profiles in database.')
        
        if not options['confirm']:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  WARNING: This will delete ALL user accounts and profiles!\n'
            ))
            self.stdout.write('To confirm deletion, run with --confirm flag:')
            self.stdout.write('  python manage.py clear_users --confirm')
            return
        
        if user_count == 0:
            self.stdout.write(self.style.SUCCESS('No users to delete.'))
            return
        
        self.stdout.write('\nDeleting all users and profiles...')
        
        # Delete UserProfiles first (they have foreign keys to User)
        deleted_profiles = UserProfile.objects.all().delete()
        self.stdout.write(f'Deleted {deleted_profiles[0]} profiles')
        
        # Delete Users
        deleted_users = User.objects.all().delete()
        self.stdout.write(f'Deleted {deleted_users[0]} users')
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully cleared all user data!\n'
            f'   - {deleted_users[0]} users deleted\n'
            f'   - {deleted_profiles[0]} profiles deleted'
        ))


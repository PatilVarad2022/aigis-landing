from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from landing.models import UserProfile

class Command(BaseCommand):
    help = 'Delete a specific user by email address'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email address of the user to delete',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion (required to actually delete)',
        )

    def handle(self, *args, **options):
        email = options['email'].lower()
        
        try:
            user = User.objects.get(email=email)
            profile = None
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                pass
            
            if not options['confirm']:
                self.stdout.write(self.style.WARNING(
                    f'\n⚠️  WARNING: This will delete user: {user.email}\n'
                    f'   Username: {user.username}\n'
                    f'   Full Name: {profile.full_name if profile else "N/A"}\n'
                    f'   Has Profile: {"Yes" if profile else "No"}\n'
                ))
                self.stdout.write('To confirm deletion, run with --confirm flag:')
                self.stdout.write(f'  python manage.py delete_user {email} --confirm')
                return
            
            # Delete profile first (if exists) - must be done before deleting user
            if profile:
                profile.delete()
                self.stdout.write(f'✓ Deleted UserProfile for {email}')
            else:
                self.stdout.write(f'  No UserProfile found for {email}')
            
            # Delete user (now safe - profile is gone)
            username = user.username
            is_superuser = user.is_superuser
            user.delete()
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Successfully deleted user!\n'
                f'   - Email: {email}\n'
                f'   - Username: {username}\n'
                f'   - Profile: {"Deleted" if profile else "None"}'
            ))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error deleting user: {e}'))


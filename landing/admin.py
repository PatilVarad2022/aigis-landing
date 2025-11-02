from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile


# Inline for UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('full_name', 'phone', 'shield_limit_percent')
    
    def has_add_permission(self, request, obj=None):
        return False


# Unregister the default User admin and register our custom one
admin.site.unregister(User)

# Custom User Admin with UserProfile inline
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'has_profile', 'full_name', 'phone', 'shield_percent', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'profile__full_name', 'profile__phone')
    ordering = ('-date_joined',)
    inlines = (UserProfileInline,)
    list_per_page = 100  # Show more users per page
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def has_profile(self, obj):
        if hasattr(obj, 'profile'):
            return format_html('<span style="color: #00FF8C;">✓ Yes</span>')
        return format_html('<span style="color: #fca5a5;">✗ No</span>')
    has_profile.short_description = 'Has Profile'
    has_profile.boolean = True
    
    def full_name(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile:
                return obj.profile.full_name
        except:
            pass
        return format_html('<span style="color: #94a3b8; font-style: italic;">No profile</span>')
    full_name.short_description = 'Full Name'
    # Removed admin_order_field to prevent errors when users don't have profiles
    
    def phone(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile:
                return obj.profile.phone or '-'
        except:
            pass
        return '-'
    phone.short_description = 'Phone'
    # Removed admin_order_field to prevent errors
    
    def shield_percent(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile:
                return f"{obj.profile.shield_limit_percent}%"
        except:
            pass
        return '-'
    shield_percent.short_description = 'Loss Shield'
    # Removed admin_order_field to prevent errors
    
    # Bulk actions for User admin
    actions = ['delete_all_users_action', 'create_missing_profiles', 'delete_orphaned_users']
    
    def delete_orphaned_users(self, request, queryset):
        """Delete users who don't have profiles (orphaned users)"""
        from django.contrib.auth.models import User
        
        # Find users without profiles (excluding superusers)
        orphaned_users = User.objects.filter(is_superuser=False).exclude(
            id__in=UserProfile.objects.values_list('user_id', flat=True)
        )
        
        count = orphaned_users.count()
        if count > 0:
            orphaned_users.delete()
            self.message_user(request, f"Deleted {count} orphaned user(s) without profiles.")
        else:
            self.message_user(request, "No orphaned users found (all users have profiles or are superusers).")
    delete_orphaned_users.short_description = "Delete orphaned users (users without profiles)"
    
    def create_missing_profiles(self, request, queryset):
        """Create UserProfile for users who don't have one"""
        created = 0
        for user in queryset:
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(
                    user=user,
                    full_name=user.email.split('@')[0],  # Use email prefix as default name
                    phone='',
                    shield_limit_percent=10
                )
                created += 1
        
        self.message_user(request, f"Created {created} profile(s) for users without profiles.")
    create_missing_profiles.short_description = "Create profiles for selected users (if missing)"
    
    def delete_all_users_action(self, request, queryset):
        """Delete ALL users and profiles - USE WITH CAUTION!"""
        from django.contrib.auth.models import User
        from .models import UserProfile
        
        total_users = User.objects.count()
        total_profiles = UserProfile.objects.count()
        
        # Don't delete superusers - only regular users
        deleted_users = User.objects.filter(is_superuser=False).delete()[0]
        deleted_profiles = UserProfile.objects.count()
        
        # Recalculate after deletion
        remaining_users = User.objects.count()
        
        self.message_user(
            request,
            f"Deleted {deleted_users} regular user(s) and {deleted_profiles} profile(s). "
            f"{remaining_users} user(s) remain (superusers preserved).",
            level='warning'
        )
    delete_all_users_action.short_description = "⚠️ DELETE ALL REGULAR USERS (keeps superusers)"


# Register the custom User admin
admin.site.register(User, CustomUserAdmin)


# UserProfile Admin with full CRUD capabilities
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_display', 'phone', 'shield_limit_percent_display', 'signup_date', 'actions_column')
    list_filter = ('shield_limit_percent', 'user__date_joined')
    search_fields = ('full_name', 'user__email', 'phone', 'user__username')
    ordering = ('-user__date_joined',)
    list_per_page = 25
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'phone')
        }),
        ('Trading Configuration', {
            'fields': ('shield_limit_percent',),
            'description': 'Loss Shield percentage (5-20%)'
        }),
    )
    
    readonly_fields = ('user',)
    
    def email_display(self, obj):
        return obj.user.email
    email_display.short_description = 'Email'
    email_display.admin_order_field = 'user__email'
    
    def shield_limit_percent_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            '#00FF8C' if 5 <= obj.shield_limit_percent <= 10 else '#0067FF',
            obj.shield_limit_percent
        )
    shield_limit_percent_display.short_description = 'Loss Shield'
    shield_limit_percent_display.admin_order_field = 'shield_limit_percent'
    
    def signup_date(self, obj):
        return obj.user.date_joined.strftime('%Y-%m-%d %H:%M')
    signup_date.short_description = 'Signup Date'
    signup_date.admin_order_field = 'user__date_joined'
    
    def actions_column(self, obj):
        return format_html(
            '<a href="/admin/landing/userprofile/{}/change/" class="button">Edit</a> | '
            '<a href="/admin/landing/userprofile/{}/delete/" class="button">Delete</a>',
            obj.id, obj.id
        )
    actions_column.short_description = 'Actions'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    # Removed changelist_view - was causing issues
    
    # Bulk actions
    actions = ['export_selected_profiles', 'delete_selected', 'delete_all_users']
    
    def delete_all_users(self, request, queryset):
        """Delete ALL users and profiles - USE WITH CAUTION!"""
        from django.contrib.auth.models import User
        
        total_users = User.objects.count()
        total_profiles = UserProfile.objects.count()
        
        # Don't delete superusers - only regular users and their profiles
        # Delete all regular users (this will cascade delete profiles)
        result = User.objects.filter(is_superuser=False).delete()
        deleted_count = result[0] if isinstance(result, tuple) else 0
        
        self.message_user(
            request,
            f"Successfully deleted {deleted_count} regular user(s) and all associated profile(s). Superusers preserved.",
            level='warning'
        )
    delete_all_users.short_description = "⚠️ DELETE ALL REGULAR USERS (keeps superusers)"
    
    def export_selected_profiles(self, request, queryset):
        """Export selected profiles to a simple text format"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_profiles.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Email', 'Phone', 'Loss Shield %', 'Signup Date'])
        
        for profile in queryset:
            writer.writerow([
                profile.full_name,
                profile.user.email,
                profile.phone or '',
                profile.shield_limit_percent,
                profile.user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    export_selected_profiles.short_description = "Export selected profiles to CSV"
    
    def delete_selected(self, request, queryset):
        """Delete selected profiles and their associated users"""
        count = 0
        users_deleted = set()
        for profile in queryset:
            user = profile.user
            user_id = user.id
            if user_id not in users_deleted:
                user.delete()  # This will cascade delete the profile
                users_deleted.add(user_id)
                count += 1
        
        self.message_user(request, f"Successfully deleted {count} profile(s) and associated user(s).")
    delete_selected.short_description = "Delete selected profiles (and users)"

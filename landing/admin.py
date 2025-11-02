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


# Custom User Admin with UserProfile inline
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'shield_percent', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'profile__full_name', 'profile__phone')
    ordering = ('-date_joined',)
    inlines = (UserProfileInline,)
    
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
    
    def full_name(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.full_name
        return '-'
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'profile__full_name'
    
    def phone(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.phone or '-'
        return '-'
    phone.short_description = 'Phone'
    phone.admin_order_field = 'profile__phone'
    
    def shield_percent(self, obj):
        if hasattr(obj, 'profile'):
            return f"{obj.profile.shield_limit_percent}%"
        return '-'
    shield_percent.short_description = 'Loss Shield'
    shield_percent.admin_order_field = 'profile__shield_limit_percent'


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
    
    # Bulk actions
    actions = ['export_selected_profiles', 'delete_selected']
    
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
        for profile in queryset:
            profile.user.delete()  # This will cascade delete the profile
            count += 1
        
        self.message_user(request, f"Successfully deleted {count} profile(s) and associated user(s).")
    delete_selected.short_description = "Delete selected profiles (and users)"

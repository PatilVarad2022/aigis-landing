from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=10, blank=True)
    # Shield limit as percent, constrained 5-20 inclusive in validation layer
    shield_limit_percent = models.PositiveSmallIntegerField(default=10)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.user.email})"


class PendingEmail(models.Model):
    """Queue for emails to be sent later (prevents 502 errors during signup)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_type = models.CharField(max_length=50, default='welcome')  # 'welcome' or 'admin_notification'
    email_data = models.JSONField()  # Store email content and details
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sent', 'created_at']),
        ]
    
    def __str__(self):
        return f"PendingEmail: {self.email_type} for {self.user.email} (sent={self.sent})"
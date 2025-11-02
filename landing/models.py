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

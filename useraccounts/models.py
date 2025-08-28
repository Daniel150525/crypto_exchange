from django.db import models
from django.conf import settings
from market.models import Currency

class UserProfile(models.Model):
    """Rozšíření uživatelského účtu o profil (2FA a oblíbené měny)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    two_factor_enabled = models.BooleanField(default=False)
    favorite_currencies = models.ManyToManyField(
        Currency,
        blank=True,
        related_name="fans"
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
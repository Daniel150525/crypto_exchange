from django.apps import AppConfig

class UseraccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "useraccounts"
    label = "useraccounts"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from .models import UserProfile

        User = get_user_model()

        @receiver(post_save, sender=User)
        def create_profile(sender, instance, created, **kwargs):
            if created:
                UserProfile.objects.create(user=instance)
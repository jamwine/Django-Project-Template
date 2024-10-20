import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from django_project_name.settings.base import AUTH_USER_MODEL
from django_apps.profiles.models import Profile

logger = logging.getLogger(__name__)

# User = get_user_model()

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            logger.info(f"Profile for {instance}'s has been created.")
        except Exception as e:
            logger.error(f"Error creating profile for {instance}: {e}")
            raise e
    else:
        # Check if profile already exists
        if not hasattr(instance, 'profile'):
            try:
                Profile.objects.create(user=instance)
                logger.info(f"Profile for {instance}'s has been created.")
            except Exception as e:
                logger.error(f"Error creating profile for {instance}: {e}")
                raise e

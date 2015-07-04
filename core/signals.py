from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import McUser

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = McUser.objects.get_or_create(user=instance)

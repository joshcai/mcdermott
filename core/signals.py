from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import McUser
from util import normalize_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  profile, created = McUser.objects.get_or_create(user=instance)
  profile.norm_name = normalize_name(instance.get_full_name())
  profile.save()

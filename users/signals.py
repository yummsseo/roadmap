from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
  # created가 True면 새로운 User가 생성된 것
  if created:
    UserProfile.objects.create(user = instance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Profile
from reviews.models import Comment, Like


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)

        channel_layer = get_channel_layer()
        group_name = "user-notifications"
        event = {"type": "user_joined", "text": instance.username}
        async_to_sync(channel_layer.send)(group_name, event)


@receiver(post_save, sender=Comment)
def receive_comment(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        owner = instance.review.profile
        group_name = f"{owner.name}-notifications"
        event = {"type": "recieve_comment", "instance": instance}
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_save, sender=Like)
def recieve_like(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        owner = instance.review.profile
        group_name = f"{owner.name}-notifications"
        event = {"type": "recieve_like", "instance": instance}
        async_to_sync(channel_layer.group_send)(group_name, event)

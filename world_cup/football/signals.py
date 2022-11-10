import pickle

from django.db.models.signals import post_save
from django.dispatch import receiver

from football.models import Match
from football.tasks import calculate


@receiver(post_save, sender=Match)
def update_concurrent_players(sender, instance, *args, **kwargs) -> None:
    print("update_concurrent_players")
    calculate.delay(match=instance.id)



from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from expenses.services import seed_default_categories


@receiver(post_save, sender=User)
def create_default_categories(sender, instance: User, created: bool, **kwargs) -> None:
    if created:
        seed_default_categories(instance)

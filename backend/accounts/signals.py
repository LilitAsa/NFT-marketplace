from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile 

@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance: User, created: bool, **kwargs):
    """
    На любое сохранение пользователя убеждаемся, что профиль есть.
    При создании — создаём с безопасными дефолтами,
    при последующих сохр. просто ничего не делаем.
    """
    defaults = dict(
        display_name="",
        bio="",
        website="",
        twitter="",
        wallet_address="",
        nfts_collected=0,
        nfts_created=0,
        followers=0,
        following=0,
    )
    try:
        UserProfile.objects.get_or_create(user=instance, defaults=defaults)
    except Exception:
        pass
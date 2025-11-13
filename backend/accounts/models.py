from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.validators import URLValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role="collector", **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password,role="admin", **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("collector", _("Collector")),
        ("pro", _("Pro User")),
        ("admin", _("Administrator")),
    ]
    
    username = models.CharField(_("Username"), max_length=150, unique=True)
    email = models.EmailField(_("Email"), unique=True)
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default="collector")
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    first_name = models.CharField(_("First name"),max_length=150, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(_("Last Login"), auto_now=True, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    telegram_chat_id = models.CharField(_("Telegram Chat ID"), max_length=50, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
        
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    token_type = models.CharField(max_length=10, choices=[('email', 'Email'), ('phone', 'Phone')])
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timedelta(hours=1)
    

def avatar_upload_path(instance, filename):
    return f"avatars/{instance.user_id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    website = models.URLField(blank=True, validators=[URLValidator()])
    twitter = models.CharField(max_length=50, blank=True)
    wallet_address = models.CharField(max_length=100, blank=True, db_index=True)

    # агрегированные счетчики (опционально, можно денормализовать)
    nfts_collected = models.PositiveIntegerField(default=0)
    nfts_created = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile<{self.user_id}>"
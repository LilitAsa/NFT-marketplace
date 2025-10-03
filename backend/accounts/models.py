from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


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
        return self.create_user(username, email, password,role="pro", **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("collector", _("Collector")),
        ("pro", _("Pro User")),
    ]
    
    username = models.CharField(_("Username"), max_length=150, unique=True)
    email = models.EmailField(_("Email"), unique=True)
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default="collector")
    is_active = models.BooleanField(_("Is active"), default=True, null=True, blank=True)
    is_staff = models.BooleanField(_("Is staff"), default=False, null=True, blank=True)
    first_name = models.CharField(_("First name"),max_length=150, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(_("Last Login"), auto_now=True, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)


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
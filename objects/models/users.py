from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Custom UserManager model."""

    def create_user(self, email, full_name, password=None, **extra_field):
        if not email:
            pass


class User(AbstractBaseUser, PermissionsMixin):
    """Custom model for User objects."""

    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='email address',
    )
    full_name = models.CharField(max_length=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None  # For using email as username
    email = models.EmailField(_('email address'), unique=True)
    is_medical_staff = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)
    contact_detail = models.CharField(_('contact detail'), max_length=25)
    address = models.TextField(_('address'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

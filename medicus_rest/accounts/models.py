from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomAccountManager


class Account(AbstractUser):
    username = None  # For using email as username
    email = models.EmailField(_('email address'), unique=True)
    designation = models.CharField(_('designation'), max_length=70)
    is_employee = models.BooleanField(default=False)
    organisation = models.CharField(
        _('organisation'),
        max_length=120,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

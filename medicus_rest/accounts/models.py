from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _

from uuid import uuid4
from .managers import CustomUserManager


class User(AbstractUser):
    username = None  # For using email as username
    email = models.EmailField(_('email address'), unique=True)
    contact_detail = models.CharField(_('contact detail'), max_length=25)
    address = models.TextField(_('address'))

    class UserType(models.TextChoices):
        MEDICAL_STAFF = 'MS', _('MS')
        ORGANISATION = 'OR', _('OR')

    user_type = models.CharField(
        _('select type of user'),
        max_length=5,
        choices=UserType.choices,
        null=True, default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_auth_token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token.key


class Organisation(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    description = models.TextField(
        _('proper description of organisation'),
    )
    short_description = models.CharField(
        _('short description of organisation (300 characters)'),
        max_length=300
    )


class MedicalStaff(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    organisation = models.OneToOneField(
        'Organisation', on_delete=models.DO_NOTHING
    )
    role = models.CharField(_('role in organisation'), max_length=30)
    speciality = models.CharField(
        _('medical speciality, if any'), max_length=30, blank=True,
        default='',
    )

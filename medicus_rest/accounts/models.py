from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _

from uuid import uuid4
from .managers import (
    CustomUserManager, OrganizationManager,
    MedicalStaffManager
)


class User(AbstractUser):
    username = None  # For using email as username
    email = models.EmailField(_('email address'), unique=True)
    contact_detail = models.CharField(_('contact detail'), max_length=25)
    address = models.OneToOneField(
        'Address', on_delete=models.DO_NOTHING)

    class UserType(models.TextChoices):
        MEDICAL_STAFF = 'MS', _('MS')
        organization = 'OR', _('OR')

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
        return "< ({}) User ({}) >".format(self.id, self.email)

    def get_auth_token(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token.key

    def get_complete_user_type(self):
        if self.user_type == 'MS':
            return "Medical Staff"

        if self.user_type == 'OR':
            return "organization"


class Address(models.Model):
    street = models.CharField(_('street name'), max_length=60)
    city = models.CharField(_('City name'), max_length=50)
    state = models.CharField(_('State name'), max_length=50)
    country = models.CharField(_('Country name'), max_length=50, default='US')
    pincode = models.CharField(_('pincode'), max_length=10)

    def __str__(self):
        return "<({}) Address {}, {} - {}, {}, {}.".format(
            self.id, self.street, self.city, self.pincode,
            self.state, self.country)


class Organization(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    description = models.TextField(
        _('proper description of organization'),
    )

    objects = OrganizationManager()

    def __str__(self):
        return "< ({}) organization's {}>".format(self.id, self.user.email)


class MedicalStaff(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    organization = models.OneToOneField(
        'organization', on_delete=models.DO_NOTHING
    )
    role = models.CharField(_('role in organization'), max_length=30)
    speciality = models.CharField(
        _('medical speciality, if any'), max_length=30, blank=True,
        default='',
    )

    objects = MedicalStaffManager()

    def __str__(self):
        return "< ({}) Medical Staff {} of {}>".format(
            self.id, self.user.email, self.organization.organization_name
        )

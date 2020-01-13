from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class Address(models.Model):
    address = models.TextField(_('Entire address'))
    country = models.CharField(_('Country name'), max_length=50, default='US')
    pincode = models.CharField(_('pincode'), max_length=10)

    def __str__(self):
        return "<({}) Address {}, {}.".format(
            self.id, self.pincode, self.country
        )


class User(AbstractUser):
    username, first_name, last_name = None, None, None  # exclude fields
    email = models.EmailField(_('email address'), unique=True)
    contact_detail = models.CharField(_('contact detail'), max_length=25)
    address = models.OneToOneField('Address', on_delete=models.DO_NOTHING)
    organization = models.OneToOneField(
        'organization.Organization', on_delete=models.DO_NOTHING,
        null=True, default=None, related_name='to_organization',
    )
    medical_staff = models.OneToOneField(
        'medical_staff.MedicalStaff', on_delete=models.DO_NOTHING,
        null=True, default=None, related_name='to_medical_staff',
    )

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
        token, created = Token.objects.get_or_create(user=self)
        return token.key

    def get_user_type(self):
        if self.user_type == 'MS':
            return self.medical_staff

        if self.user_type == 'OR':
            return self.organization

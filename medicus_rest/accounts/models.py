from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomAccountManager
# class Account(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     designation = models.CharField(max_length=70)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)
#     is_employee = models.BooleanField(default=False)

#     def __str__(self):
#         return "{} {}".format(self.first_name,self.last_name)

class Account(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    designation = models.CharField(max_length=70)
    organisation = models.CharField(max_length=120, default=None)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomAccountManager()
    
    def __str__(self):
        return self.email
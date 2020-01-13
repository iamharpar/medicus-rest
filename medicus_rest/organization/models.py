from django.db import models
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Organization(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(_('organization name'), max_length=30, unique=True)
    description = models.TextField(
        _('proper description of organization'),
    )

    def __str__(self):
        return "< ({}) organization>".format(self.name)

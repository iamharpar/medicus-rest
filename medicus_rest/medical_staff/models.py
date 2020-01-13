from django.db import models
from django.utils.translation import ugettext_lazy as _

from uuid import uuid4
# Create your models here.


class MedicalStaff(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(_('medical staff name'), max_length=50)
    is_verified = models.BooleanField(default=False)
    organization = models.ForeignKey(
        'organization.Organization', on_delete=models.DO_NOTHING
    )
    role = models.CharField(_('role in organization'), max_length=30)
    speciality = models.CharField(
        _('medical speciality, if any'), max_length=30, blank=True,
        default='',
    )

    def __str__(self):
        return "< ({}) Medical Staff of {}>".format(
            self.name, str(self.organization),
        )

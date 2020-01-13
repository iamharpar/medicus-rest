from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Patient(models.Model):
    name = models.CharField(_('patient name'), max_length=50)
    weight = models.DecimalField(
        _('patient weight (lb)'), decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0)]
    )
    height = models.DecimalField(
        _('patient height (inch)'), decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0)]
    )

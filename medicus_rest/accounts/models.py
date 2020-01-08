from django.db import models

# Create your models here.
class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=70)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)
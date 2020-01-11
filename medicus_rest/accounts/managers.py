from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.db import models
from uuid import uuid4


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_organisation', False)
        extra_fields.setdefault('is_medical_staff', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(Q(**{self.model.EMAIL_FIELD: username}))


class OrganisationManager(models.Manager):
    def _update_or_create(self, user, **extra_fields):
        organisation = self.model(user=user, **extra_fields)
        organisation.save()
        return organisation

    def create_organisation(self, user, **extra_fields):
        return self._update_or_create(user, **extra_fields)

class MedicalStaffManager(models.Manager):
    def _update_or_create(self, user, organisation, **extra_fields):
        medicalStaff = self.model(user=user, organisation=organisation, **extra_fields)
        medicalStaff.save()
        return medicalStaff

    def create_medicalstaff(self, user, organisation, **extra_fields):
        return self._update_or_create(user, organisation, **extra_fields)

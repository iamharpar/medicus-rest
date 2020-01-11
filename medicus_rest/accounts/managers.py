from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, address, **extra_fields):
        if not email:
            raise ValueError('email must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('user_type', None)
        user = self.model(email=email, address=address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, address, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, address, **extra_fields)

    def create_superuser(self, email, password, address, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, address, **extra_fields)

    def update_user_address(self, email, address):
        user = super().filter(email)
        if user:
            user = user.get(email=email)
            setattr(user, 'address', address)
            user.save(using=self._db)
            return user
        raise ObjectDoesNotExist('user does not exist')

    def get_by_natural_key(self, username):
        return self.get(Q(**{self.model.EMAIL_FIELD: username}))


class OrganizationManager(models.Manager):
    def _create_organization(self, user, **extra_fields):
        organization = self.model(user=user, **extra_fields)
        organization.save()
        return organization

    def _update_organization(self, user, **extra_fields):
        organization = super().filter(user=user)
        if organization:
            organization.update(**extra_fields)
            return organization
        raise ObjectDoesNotExist('organization does not exist')

    def update_organization(self, user, **extra_fields):
        return self._update_organization(user, **extra_fields)

    def create_organization(self, user, **extra_fields):
        return self._create_organization(user, **extra_fields)


class MedicalStaffManager(models.Manager):
    def _create_medicalstaff(self, user, org, **extra_fields):
        medical_staff = self.model(
            user=user, organization=org, **extra_fields)
        medical_staff.save(using=self._db)
        return medical_staff

    def _update_medicalstaff(self, user, **extra_fields):
        medical_staff = super().filter(user=user)
        if medical_staff:
            medical_staff.update(**extra_fields)
            return medical_staff
        raise ObjectDoesNotExist("given staff object doesn't exist")

    def update_medicalstaff(self, user, **extra_fields):
        return self._update_medicalstaff(user, **extra_fields)

    def update_staff_organization(self, user, org):
        medical_staff = super().filter(user=user)
        if medical_staff:
            medical_staff = medical_staff.get(user=user)
            setattr(medical_staff, 'organization', org)
            medical_staff.save(using=self._db)
            return medical_staff
        raise ObjectDoesNotExist("given staff object doesn't exist")

    def create_medicalstaff(self, user, org, **extra_fields):
        return self._create_medicalstaff(user, org, **extra_fields)

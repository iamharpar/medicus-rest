from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **extra_fields):
        if "email" not in extra_fields:
            raise ValueError('email must be set')

        email = extra_fields.pop('email')  # remove address in case it's passed
        password = extra_fields.pop('password')
        email = self.normalize_email(email)
        extra_fields.setdefault('user_type', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        print(extra_fields)

        return self._create_user(**extra_fields)

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
        raise ObjectDoesNotExist('user with {} does not exist'.format(email))

    def get_by_natural_key(self, username):
        return self.get(Q(**{self.model.EMAIL_FIELD: username}))

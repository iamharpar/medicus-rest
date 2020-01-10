from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def on_user_logout(sender, user, request, **kwargs):
    pass

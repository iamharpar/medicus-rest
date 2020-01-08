from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


@admin.register(Account)
class AccountAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'designation', 'organisation', 'is_employee')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups', 'user_permissions')}),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'designation', 'organisation', 'is_employee', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name',
                     'designation', 'organisation')
    ordering = ('email',)

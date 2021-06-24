from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from users.models import User


class UserAdmin(BaseUserAdmin):
    ordering = ('id',)

    list_display = ('email', 'username',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'image', 'bio')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')},),
        (_('Important Dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2',)
                }
         ),
    )

admin.site.register(User, UserAdmin)

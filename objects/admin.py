from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from objects.models.stores import EcommerceStore
from objects.models.users import User


class UserAdmin(BaseUserAdmin):
    '''Admin for User object.'''

    ordering = ['id']
    list_display = ['email', 'full_name']
    list_filter = ['email', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')},
        ),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['date_joined', 'last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'full_name',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


class EcommerceStoreAdmin(admin.ModelAdmin):
    '''Admin for EcommerceStore object.'''

    ordering = ['id']
    list_display = ['name', 'domain']
    fieldsets = (
        (None, {'fields': ('name', 'domain', 'discovery_url')}),
        (
            _('Scraper Import'),
            {'fields': ('package_name', 'module_name', 'class_name')}
        ),
        (
            _('Dates'),
            {'fields': ('created', 'last_scrape_start', 'last_scrape_end')}
        ),
        (_('Status'), {'fields': ('is_active',)}),
    )
    readonly_fields = ['created', 'last_scrape_start', 'last_scrape_end']


admin.site.register(User, UserAdmin)
admin.site.register(EcommerceStore, EcommerceStoreAdmin)
from django.contrib import admin
from .models import RegularAccount, BusinessAccount, BillingAddress
from django.conf import settings
from .models import RegularAccount
from django.contrib.auth.admin import UserAdmin
from .forms import RegularAccountCreationForm, RegularAccountChangeForm


# Register your models here.


admin.site.register(BusinessAccount)
admin.site.register(BillingAddress)


class RegularAccountAdmin(UserAdmin):
    add_form = RegularAccountCreationForm
    form = RegularAccountChangeForm
    model = RegularAccount
    list_display = ('username', 'first_name', 'last_name',
                    'is_staff', 'is_active',)
    list_filter = ('username', 'first_name', 'last_name',
                   'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password',
         'email', 'first_name', 'last_name', 'isbusiness', 'favourite_shops')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'username', 'favourite_shops')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(RegularAccount, RegularAccountAdmin)

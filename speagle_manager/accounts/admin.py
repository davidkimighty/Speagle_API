from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import UserCreationForm, UserChangeForm
# from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm # update view
    add_form = UserCreationForm # create view

    list_display = ('email', )
    list_filter = ('is_active', 'is_staff', 'is_superuser', )

    fieldsets = (
        (None, {
            'fields': ('email', 'password', ),
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'gender', 'dob', 'country', 'photo', ),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', ),
        }),
        # (_('Important dates'), {
        #     'fields': ('last_login', 'date_joined', ),
        # }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )

    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
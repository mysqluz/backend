from .models import User, Category, Problem, Task, News

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'email', 'avatar', 'ball')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'avatar', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'fullname', 'is_staff', 'ball')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('-ball',)


admin.site.register(User, UserAdminCustom)
admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Task)
admin.site.register(News)

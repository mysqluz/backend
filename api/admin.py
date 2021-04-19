from .models import User, Category, Problem, Task, News

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Task)
admin.site.register(News)

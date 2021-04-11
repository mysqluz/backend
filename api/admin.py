from django.contrib import admin
from .models import User, Category, Problem, Task, News

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Task)
admin.site.register(News)

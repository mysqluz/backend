from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='static/uploads')
    role = models.IntegerField(choices=((0, 'ADMIN'), (1, 'USER')), default=1)
    ball = models.IntegerField(default=0)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_authenticated and self.is_active and self.is_staff


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        print(self.slug)
        super(Category, self).save(*args, **kwargs)


class Problem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    content = models.TextField()
    dump_file_src = models.CharField(max_length=255)
    permissions = models.JSONField()
    ball = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.RESTRICT)


class Task(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tasks')
    status = models.IntegerField(choices=((0, 'IN QUEUE'),), default=0)
    source = models.TextField()


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    views = models.IntegerField(default=0)

from time import time

from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify

from checker import tester


def problem_dump_directory(problem, filename):
    return f"static/dumps/{filename}"


class Constants:
    PERMISSION_SELECT = 0
    PERMISSION_EXECUTE = 1
    TASK_IN_QUEUE = -2
    TASK_RUNNING = -1
    TASK_JUDGEMENT_FAILED = 0
    TASK_ACCEPTED = 1
    TASK_WRONG_ANSWER = 2


class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='static/uploads')
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

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        print(self.slug)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Problem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    content = models.TextField()
    dump = models.TextField()
    answer = models.TextField()
    permissions = models.IntegerField(choices=(
        (Constants.PERMISSION_SELECT, 'SELECT'),
        (Constants.PERMISSION_EXECUTE, 'EXECUTE (INSERT, UPDATE, DELETE)'),
    ))
    execute_table = models.CharField(max_length=255, null=True, blank=True)
    ball = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    def clean(self):
        if self.permissions == Constants.PERMISSION_EXECUTE and not self.execute_table:
            raise ValidationError("Execute table required on Permission Execute")


class Task(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.DO_NOTHING, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tasks')
    status = models.IntegerField(choices=(
        (Constants.TASK_IN_QUEUE, 'IN QUEUE'),
        (Constants.TASK_RUNNING, 'RUNNING'),
        (Constants.TASK_JUDGEMENT_FAILED, 'JUDGEMENT FAILED'),
        (Constants.TASK_ACCEPTED, 'ACCEPTED'),
        (Constants.TASK_WRONG_ANSWER, 'WRONG ANSWER'),
    ), default=Constants.TASK_IN_QUEUE)
    source = models.TextField()

    def __str__(self):
        return f"{self.problem} - {self.user}"


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


@receiver(models.signals.post_save, sender=Task)
def execute_after_save(sender, instance: Task, created, *args, **kwargs):
    if created:
        t1 = time()
        instance.status = Constants.TASK_RUNNING
        instance.save()
        try:
            _tester = tester.Tester(instance)
            if _tester.test():
                instance.status = Constants.TASK_ACCEPTED
            else:
                instance.status = Constants.TASK_WRONG_ANSWER
        except Exception as e:
            instance.status = Constants.TASK_JUDGEMENT_FAILED
            print('CHECK FAILED', e)
        instance.save()
        print('Checked in', time() - t1)
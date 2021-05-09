from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import User, Category, Problem, News, Task, Constants


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar', 'ball']


class UserRegistrationSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "avatar", "password", "confirm_password")

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True, allow_null=True)
    confirm_password = serializers.CharField(write_only=True, allow_null=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "avatar", "password", "confirm_password")

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        if 'confirm_password' in attrs:
            del attrs['confirm_password']
        if 'password' in attrs:
            attrs['password'] = make_password(attrs['password'])
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('dump', 'permissions', 'answer', 'execute_table')


class ProblemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Problem
        exclude = ('dump', 'permissions', 'answer', 'execute_table')


class ProblemWithoutCategorySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    accepted = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        exclude = ('dump', 'permissions', 'answer', 'execute_table')

    def get_accepted(self, obj: Problem):
        task = Task.objects.filter(user_id=self.context['request'].user.pk,
                                   problem=obj,
                                   status=Constants.TASK_ACCEPTED).first()
        return bool(task)


class TaskProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'title')


class CategoryProblemsSerializer(serializers.ModelSerializer):
    problems = ProblemWithoutCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    problem = TaskProblemSerializer()
    user = UserSerializer()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Task
        exclude = ('source',)

    def get_field_names(self, declared_fields, info):
        fields = super(TaskSerializer, self).get_field_names(declared_fields, info)
        if isinstance(self.instance, Task) and self.instance.user == self.context['request'].user:
            fields.append('source')
        return fields

    def get_status_text(self, obj: Task):
        return Constants.task.get(obj.status)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('user',)


class TaskWithoutUserSerializer(serializers.ModelSerializer):
    problem = TaskProblemSerializer()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Task
        exclude = ('source', 'user')

    def get_status_text(self, obj: Task):
        return Constants.task.get(obj.status)


class TaskWithoutProblemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Task
        exclude = ('source', 'problem')

    def get_status_text(self, obj: Task):
        return Constants.task.get(obj.status)


class UserTasksSerializer(serializers.ModelSerializer):
    tasks = TaskWithoutUserSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar', 'ball', 'tasks']


class ProblemTasksSerializer(serializers.ModelSerializer):
    tasks = TaskWithoutProblemSerializer(many=True)

    class Meta:
        model = Problem
        exclude = ('dump', 'permissions', 'answer', 'execute_table')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

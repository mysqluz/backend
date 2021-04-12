from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response

from api.models import Category, User, Problem, News, Task
from api.permissions import UserPermission, UserUpdatePermission, CategoryProblemNewsPermission, TaskPermission
from api.serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    TokenSerializer, CategorySerializer,
    UserSerializer, UserUpdateSerializer,
    ProblemSerializer, NewsSerializer,
    CategoryProblemsSerializer, TaskSerializer,
    UserTasksSerializer, ProblemTasksSerializer,
    TaskCreateSerializer
)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)
    http_method_names = ['get', 'head', 'options']


class UserRegistrationAPIView(CreateAPIView):
    """ Register User """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    """ Login User """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserUpdateAPIView(UpdateAPIView):
    http_method_names = ['put', 'patch']
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (UserUpdatePermission,)


class UserTokenAPIView(RetrieveDestroyAPIView):
    """Token"""
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    """Categories"""
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']


class ProblemViewSet(viewsets.ModelViewSet):
    """Problems"""
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']


class CategoryProblemsViewSet(viewsets.ModelViewSet):
    """CategoryProblems"""
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoryProblemsSerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']


class TaskViewSet(viewsets.ModelViewSet):
    """Tasks"""
    queryset = Task.objects.all()
    permission_classes = (TaskPermission,)

    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskSerializer
        return TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskCreateViewSet(viewsets.ModelViewSet):
    """TaskCreate"""
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = (TaskPermission,)

    http_method_names = ['post']


class UserTasksViewSet(viewsets.ModelViewSet):
    """UserTasks"""
    queryset = User.objects.all()
    serializer_class = UserTasksSerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']


class ProblemTasksViewSet(viewsets.ModelViewSet):
    """ProblemTasks"""
    queryset = Problem.objects.all()
    serializer_class = ProblemTasksSerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']


class NewsViewSet(viewsets.ModelViewSet):
    """News"""
    lookup_field = 'slug'
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (CategoryProblemNewsPermission,)

    http_method_names = ['get']

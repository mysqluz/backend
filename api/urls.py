"""mysqluz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers

from api.views import (
    UserViewSet, UserRegistrationAPIView,
    UserLoginAPIView, UserTokenAPIView,
    CategoryViewSet, UserUpdateAPIView,
    ProblemViewSet, NewsViewSet,
    CategoryProblemsViewSet, TaskViewSet,
    UserTasksViewSet, ProblemTasksViewSet,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<pk>', UserUpdateAPIView.as_view(), name='update'),
    path('users/<pk>/tasks', UserTasksViewSet.as_view({'get': 'retrieve'}), name='user_tasks'),
    path('auth/register/', UserRegistrationAPIView.as_view(), name="register"),
    path('auth/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('categories/<slug>/problems', CategoryProblemsViewSet.as_view({'get': 'retrieve'}), name="category_problems"),
    path('problems/<pk>/tasks', ProblemTasksViewSet.as_view({'get': 'retrieve'}), name="problem_tasks"),
]

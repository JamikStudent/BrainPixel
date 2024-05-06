"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserAPIView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/<int:user_id>/balance/', views.check_balance, name='check_balance'),
    path('users/<int:user_id>/bonus_coin/', views.bonus_coin, name='bonus_coin'),
    path('users/<int:user_id>/buy_tips/<str:type_of_tip>/', views.buy_tips, name='buy_tips'),
    path('users/<int:user_id>/buy_skin/<str:skin_name>/', views.buy_skin, name='buy_skin'),
    path('users/<int:user_id>/skin_info/', views.user_skin_info, name='user_skin_info'),
    path('users/<int:user_id>/change_skin/<str:skin_name>/', views.change_skin, name='change_skin'),
    path('use-hints/', views.use_hints_view, name='use_hints'),
    path('topics/', views.TopicList.as_view(), name='topic-list'),  # Ссылка на представление TopicList
    path('questions/', views.QuestionListAPIView.as_view(), name='question-list'),  # Ссылка на представление QuestionListAPIView
    path('submit_answers/', views.submit_answers, name='submit_answers'),
    path('v/t_auth/', include('rest_framework.urls')),
    path('v/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

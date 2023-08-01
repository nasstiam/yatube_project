"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import pytest
from django.contrib import admin
from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug>/', views.group_posts, name='group_lists'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit')

]

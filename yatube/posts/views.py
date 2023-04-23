from django.shortcuts import render

from django.http import HttpResponse


# Главная страница
def index(request):
    return HttpResponse('Главная страница')


# Страница со списком постов
def group_posts(request):
    return HttpResponse('Список постов')


# Страница с информацией об одном посте;
# view-функция принимает параметр pk из path()
def group_posts_detail(request, pk):
    return HttpResponse(f'Номер поста {pk}')

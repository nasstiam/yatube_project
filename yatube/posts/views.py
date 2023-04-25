from django.shortcuts import render

from django.http import HttpResponse


# Главная страница
def index(request):
    template = 'posts/index.html'
    return render(request, template)


# Страница со списком постов
def group_posts(request):
    template = 'posts/group_posts.html'
    return render(request, template)


# Страница с информацией об одном посте;
# view-функция принимает параметр pk из path()
def group_posts_detail(request, pk):
    return HttpResponse(f'Номер поста {pk}')

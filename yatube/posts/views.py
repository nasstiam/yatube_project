from django.shortcuts import render

from django.http import HttpResponse


# Главная страница
def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    context = {
        # В словарь можно передать переменную
        'title': title,
        # А можно сразу записать значение в словарь. Но обычно так не делают
    }
    return render(request, template, context)


# Страница со списком постов
def group_posts(request):
    template = 'posts/group_posts.html'
    title = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'title': title,
    }
    return render(request, template, context)


# Страница с информацией об одном посте;
# view-функция принимает параметр pk из path()
def group_posts_detail(request, pk):
    return HttpResponse(f'Номер поста {pk}')

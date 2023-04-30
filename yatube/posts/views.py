# posts/views.py
from django.shortcuts import render, get_object_or_404, HttpResponse
# Импортируем модель, чтобы обратиться к ней
from .models import Post, Group

def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    posts = Post.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


# Страница со списком постов
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_posts.html'
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


# Страница с информацией об одном посте;
# view-функция принимает параметр pk из path()
def group_posts_detail(request, pk):
    return HttpResponse(f'Номер поста {pk}')

# posts/views.py
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect

from .forms import PostForm, EditForm
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_posts.html'
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    template = 'posts/post_detail.html'
    posts = Post.objects.filter(text=post)[0]

    all_author_posts = Post.objects.filter(author=posts.author)

    context = {
        'posts': posts,
        'post': post,
        'all_author_posts': all_author_posts
    }
    return render(request, template, context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                new_post = form.save(commit=False)
                new_post.author_id = request.user.id
                new_post.save()
                return redirect('posts:profile', request.user.username)
            except Exception as e:
                print(e)
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = PostForm()
    template = 'posts/post_create.html'
    context = {
        'form': form,
        'title': 'Новый пост'
    }
    return render(request, template, context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            try:
                form.save()
                return redirect('posts:profile', request.user.username)
            except Exception as e:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = PostForm(instance=post)

    template = 'posts/post_edit.html'
    context = {
        'post': post,
        'form': form
    }
    return render(request, template, context)
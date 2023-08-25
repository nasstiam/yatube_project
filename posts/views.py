# posts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment, Follow
from django.core.paginator import Paginator

post_per_page = 10

@cache_page(60 * 15)
def index(request):
    authorised_user = request.user
    post_list = Post.objects.all().order_by('-created')
    paginator = Paginator(post_list, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'authorised_user': authorised_user,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    authorised_user = request.user
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_posts.html'
    posts = Post.objects.filter(group=group).order_by('-created')
    paginator = Paginator(posts, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'authorised_user': authorised_user,
        'group': group,
        'page_obj': page_obj,
        'paginator': paginator,
        'page': page_number
    }
    return render(request, template, context)


def profile(request, username):
    authorised_user = request.user
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    posts = Post.objects.filter(author=author).order_by('-created')
    paginator = Paginator(posts, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if authorised_user.is_authenticated:
        follow = Follow.objects.filter(author=author, user=authorised_user)
        follower_count = author.follower.count()
        following_count = author.following.count()
    else:
        follow = False
        follower_count = None
        following_count = None
    context = {
        'user': authorised_user,
        'page_obj': page_obj,
        'posts': posts,
        'author': author,
        'paginator': paginator,
        'follower_count': follower_count,
        'following_count': following_count,
        'follow': follow
    }
    return render(request, template, context)


def post_detail(request, post_id):
    authorised_user = request.user
    post = get_object_or_404(Post, id=post_id)
    template = 'posts/post_detail.html'
    all_author_posts = Post.objects.filter(author=post.author)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post_id)

    context = {
        'authorised_user': authorised_user,
        'post': post,
        'all_author_posts': all_author_posts.count,
        'author': post.author,
        'comment_form': comment_form,
        'comments': comments,
        'form': comment_form
    }
    return render(request, template, context)

@login_required()
def post_create(request):
    authorised_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            try:
                new_post = form.save(commit=False)
                new_post.author_id = request.user.id
                new_post.save()
                return redirect('posts:profile', username=request.user.username)
            except Exception as e:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = PostForm()
    template = 'posts/post_create.html'
    context = {
        'authorised_user': authorised_user,
        'form': form,
        'title': 'Новый пост',
    }
    return render(request, template, context)

@login_required()
def post_edit(request, post_id):
    authorised_user = request.user
    post = get_object_or_404(Post, id=post_id)
    if authorised_user.id == post.author.id:
        if request.method == 'POST':
            form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('posts:profile', username=request.user.username)
                except Exception as e:
                    form.add_error(None, 'Ошибка добавления поста')
        else:
            form = PostForm(instance=post)

        template = 'posts/post_edit.html'
        context = {
            'authorised_user': authorised_user,
            'post': post,
            'form': form,
            'is_edit': True
        }
        return render(request, template, context)


@login_required
def add_comment(request, post_id):
    authorised_user = request.user
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post_detail', post_id=post_id)
    else:
        form = CommentForm()

    template = 'posts/add_comment.html'
    context = {
        'authorised_user': authorised_user,
        'post': post,
        'form': form,
    }

    return render(request, template, context)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    authorised_user = request.user
    # ищем автора, у которого в following(в подписчиках) есть пользователь authorised_user
    post_list = Post.objects.filter(author__following__user=authorised_user).order_by('-created')
    paginator = Paginator(post_list, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'authorised_user': authorised_user,
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, 'posts/follow_index.html', context)


@login_required
def profile_follow(request, username):
    authorised_user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(author=author, user=authorised_user)
    if len(follow) == 0 and author != request.user:
        follow = Follow.objects.get_or_create(user=authorised_user, author=author)
    context = {
        'authorised_user': authorised_user,
        'author': author,
        'follow': follow,
    }
    return render(request, 'posts/follow.html', context)

@login_required
def profile_unfollow(request, username):
    # Дизлайк, отписка
    authorised_user = request.user
    author = get_object_or_404(User, username=username)
    if len(Follow.objects.filter(user=authorised_user, author=author)) > 0:
        Follow.objects.filter(user=authorised_user, author=author).delete()
    context = {
        'authorised_user': authorised_user,
        'author': author,
    }
    return render(request, 'posts/unfollow.html', context)

@login_required
def profile_following_list(request, username):
    # following = подписки
    authorised_user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(author=author)
    context = {
        'authorised_user': authorised_user,
        'author': author,
        'following': follow,
     }
    return render(request, 'posts/following_list.html', context)

@login_required
def profile_follower_list(request, username):
    # follower = подписчики
    authorised_user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=author)
    context = {
        'authorised_user': authorised_user,
        'author': author,
        'follower': follow,
     }
    return render(request, 'posts/follower_list.html', context)

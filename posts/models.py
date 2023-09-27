from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Post(CreatedModel):
    objects = None
    text = models.TextField(verbose_name='Текст', help_text='Введите текст поста')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Группа"
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media',
        blank=True
    )

    def __str__(self):
        # выводим текст поста
        return {self.text[:15]}


class Comment(CreatedModel):
    objects = None
    post = models.ForeignKey(
        Post,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Комментарий"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария', help_text='Введите текст комментария')


class Follow(models.Model):
    objects = None
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
    )
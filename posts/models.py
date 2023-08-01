from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):

    objects = None
    text = models.TextField(verbose_name='Текст', help_text='Введите текст поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
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


    def __str__(self):
        # выводим текст поста
        return f'{self.text[:15]}'




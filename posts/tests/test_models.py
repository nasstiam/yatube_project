from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост пост',
        )


    def test_models_have_correct_object_names_group(self):
        """Проверяем, что у моделей group корректно работает __str__."""
        group1 = PostModelTest.group
        self.assertEqual(str(group1), 'Тестовая группа')


    def test_models_have_correct_object_names_text(self):
        """Проверяем, что у моделей post корректно работает __str__."""

        post1 = PostModelTest.post
        self.assertEqual(str(post1), 'Тестовый пост п')
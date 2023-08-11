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

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)
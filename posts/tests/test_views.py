# deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts import models
from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='name')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        for post_id in range(10):
            Post.objects.create(
                author=cls.user,
                text=f'Text {post_id}',
                group=cls.group
            )
        cls.post = Post.objects.all()[0]


    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_posts.html': reverse('posts:group_lists', kwargs={'slug': 'Тестовый слаг'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'name'}),
            'posts/post_detail.html': (reverse('posts:post_detail', kwargs={'post_id': PostsPagesTests.post.pk})),
            'posts/post_create.html': reverse('posts:post_create'),
            'posts/post_edit.html': reverse('posts:post_edit', kwargs={'post_id': PostsPagesTests.post.pk}),
        }

        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post_list = response.context.get("page_obj")
        self.assertQuerysetEqual(post_list, Post.objects.all().order_by('-pub_date')[:10], transform=lambda x: x)

class PostsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 2 users, 2 groups and 13 posts
        cls.user1 = User.objects.create_user(username='name1')
        cls.user2 = User.objects.create_user(username='name2')
        cls.group1 = Group.objects.create(title='group1', slug='group1', description='group1')
        cls.group2 = Group.objects.create(title='group2', slug='group2', description='group2')
        posts_number_group1 = 12

        for post_id in range(posts_number_group1):
            Post.objects.create(
                author=cls.user1,
                text=f'Text {post_id}',
                group=cls.group1
            )

        Post.objects.create(
            author=cls.user2,
            text=f'Text 13',
            group=cls.group2
        )



    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)
    def test_all_pages_pagination(self):
        '''На 1й странице index, group_lists, profile должно быть 10 постов, а 2й - 2 или 1 в завис-ти от группы'''
        # словарь reverse(name) : количество постов на странице
        pages_for_test = {
            (reverse('posts:index'),): 10,
            ((reverse('posts:index') + '?page=2'),): 3,
            ((reverse('posts:group_lists', kwargs={'slug': 'group1'})),): 10,
            ((reverse('posts:group_lists', kwargs={'slug': 'group1'}) + '?page=2'),): 2,
            ((reverse('posts:group_lists', kwargs={'slug': 'group2'})),): 1,
            ((reverse('posts:profile', kwargs={'username': 'name1'})),): 10,
            ((reverse('posts:profile', kwargs={'username': 'name1'}) + '?page=2'),): 2,
            ((reverse('posts:profile', kwargs={'username': 'name2'})),): 1
        }

        for reverse_name, num_pages in pages_for_test.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(*reverse_name)
                self.assertEqual(len(response.context['page_obj']), num_pages)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:group_lists', kwargs={'slug': 'group2'}))
        post_list = response.context.get("page_obj")
        self.assertQuerysetEqual(post_list, Post.objects.filter(group=PostsViewsTest.group2), transform=lambda x: x)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:profile', kwargs={'username': 'name1'}))
        post_list = response.context.get("page_obj")
        self.assertQuerysetEqual(post_list, Post.objects.filter(author=PostsViewsTest.user1).order_by('-pub_date')[0:10], transform=lambda x: x)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': 10}))
        post_10 = response.context.get('post')
        post_fields_for_test = {
        'Text 9': post_10.text,
        'name1': post_10.author.username,
        'group1': post_10.group.title
        }

        for value, expected in post_fields_for_test.items():
            self.assertEquals(value, expected)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response_create = self.authorized_client.get(reverse('posts:post_create'))
        post_create_fields_for_test = {
        'text': forms.fields.CharField,
        'group': forms.models.ModelChoiceField,
        }

        for value, expected in post_create_fields_for_test.items():
            with self.subTest(value=value):
                form_field_create = response_create.context.get('form').fields.get(value)
                self.assertIsInstance(form_field_create, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response_edit = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': 10}))
        post_edit_fields_for_test = {
        'text': forms.fields.CharField,
        'group': forms.models.ModelChoiceField,
        }

        for value, expected in post_edit_fields_for_test.items():
            with self.subTest(value=value):
                form_field_edit = response_edit.context.get('form').fields.get(value)
                self.assertIsInstance(form_field_edit, expected)

    def test_post_with_group_correct_pages(self):
        """если указать группу поста, то пост появляется на странице group_lists, index, profile, и не появляется на
        странице другой группы"""
        posts_number = len(Post.objects.all())
        posts_number_group2 = len(Post.objects.filter(group=PostsViewsTest.group2))
        posts_number_group1 = len(Post.objects.filter(group=PostsViewsTest.group1))
        posts_number_user2 = len(Post.objects.filter(author=PostsViewsTest.user2))
        Post.objects.create(
            author=PostsViewsTest.user2,
            text=f'Text 14',
            group=PostsViewsTest.group2
        )
        self.assertEquals(Post.objects.count(), posts_number + 1)
        self.assertEquals(Post.objects.filter(group=PostsViewsTest.group2).count(), posts_number_group2 + 1)
        self.assertNotEquals(Post.objects.filter(group=PostsViewsTest.group1).count(), posts_number_group1 + 1)
        self.assertEquals(Post.objects.filter(author=PostsViewsTest.user2).count(), posts_number_user2 + 1)




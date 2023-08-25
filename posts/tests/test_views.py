# deals/tests/test_views.py
import os

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group, Comment, Follow

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
        cache.clear()
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
        self.assertQuerysetEqual(post_list, Post.objects.all().order_by('-created')[:10], transform=lambda x: x)


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
                group=cls.group1,
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

        response_num = self.guest_client.get((reverse('posts:group_lists', kwargs={'slug': 'group1'})))
        self.assertEqual(len(response_num.context.get('page_obj')), 10)

        for reverse_name, num_pages in pages_for_test.items():
            cache.clear()
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(*reverse_name)
                self.assertEqual(len(response.context.get('page_obj')), num_pages)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:group_lists', kwargs={'slug': 'group2'}))
        post_list = response.context.get("page_obj")
        self.assertQuerysetEqual(post_list, Post.objects.filter(group=PostsViewsTest.group2), transform=lambda x: x)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'name1'}))
        post_list = response.context.get("page_obj")
        self.assertQuerysetEqual(post_list, Post.objects.filter(author=PostsViewsTest.user1).order_by('-created')[0:10], transform=lambda x: x)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': 10}))
        post_10 = response.context.get('post')

        self.assertEqual('Text 9', post_10.text)
        self.assertEqual('name1', post_10.author.username)
        self.assertEqual('group1', post_10.group.title)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response_create = self.authorized_client.get(reverse('posts:post_create'))

        form_field_edit_text = response_create.context.get('form').fields.get('text')
        form_field_edit_group = response_create.context.get('form').fields.get('group')
        self.assertIsInstance(form_field_edit_text, forms.fields.CharField)
        self.assertIsInstance(form_field_edit_group, forms.models.ModelChoiceField)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response_edit = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': 10}))

        form_field_edit_text = response_edit.context.get('form').fields.get('text')
        form_field_edit_group = response_edit.context.get('form').fields.get('group')
        self.assertIsInstance(form_field_edit_text, forms.fields.CharField)
        self.assertIsInstance(form_field_edit_group, forms.models.ModelChoiceField)

    def test_post_with_group_correct_pages(self):
        """если указать группу поста, то пост появляется на странице group_lists, index, profile, и не появляется на
        странице другой группы"""
        posts_number = len(Post.objects.all())
        posts_number_group2 = len(Post.objects.filter(group=PostsViewsTest.group2))
        posts_number_group1 = len(Post.objects.filter(group=PostsViewsTest.group1))
        posts_number_user2 = len(Post.objects.filter(author=PostsViewsTest.user2))

        Post.objects.create(
            author=PostsViewsTest.user2,
            text='Text 14',
            group=PostsViewsTest.group2,
            image=SimpleUploadedFile(name='logo.png', content=open(os.getcwd()+'/posts/tests/img/logo.png', 'rb').read(), content_type='image/png')
        )
        # при отправке поcта с группой\картинкой через форму PostForm создаётся запись в базе данных
        # на странице group_lists, index, profile
        self.assertEquals(Post.objects.count(), posts_number + 1)
        self.assertEquals(Post.objects.filter(group=PostsViewsTest.group2).count(), posts_number_group2 + 1)
        self.assertEquals(Post.objects.filter(group=PostsViewsTest.group1).count(), posts_number_group1)
        self.assertEquals(Post.objects.filter(author=PostsViewsTest.user2).count(), posts_number_user2 + 1)

        # при отправке поcта с картинкой через форму PostForm запись видна на странице post_detail
        response14 = self.guest_client.get(reverse('posts:post_detail', kwargs={'post_id': 14}))
        post_14 = response14.context.get('post')
        self.assertIsNotNone(post_14.image, 'картинка не появляется на странице post_detail')

    def test_comment_auth_user(self):
        """Комментировать посты может только авторизованный пользователь"""
        comments_number = Comment.objects.all().count()
        Comment.objects.create(
            post=Post.objects.all().order_by('-created')[0],
            author=PostsPagesTests.user,
            text='Authorized client comment'
        )
        self.assertEquals(Comment.objects.all().count(), comments_number+1)

    def test_comment_guest_client(self):
        """Неавторизованному пользователю не достпуна страница /comment/"""
        self.guest_client.post(reverse('posts:add_comment', kwargs={'post_id': 1}))
        self.assertFalse(Comment.objects.filter(post_id=1).exists())

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response1 = self.authorized_client.get(reverse('posts:index'))
        posts1 = response1.content
        Post.objects.create(
            author=PostsViewsTest.user2,
            text='Text 14',
            group=PostsViewsTest.group2,
            )
        response2 = self.authorized_client.get(reverse('posts:index'))
        posts2 = response2.content
        self.assertEquals(posts1, posts2)
        cache.clear()
        response3 = self.authorized_client.get(reverse('posts:index'))
        posts3 = response3.context
        self.assertNotEquals(posts3, posts2)

    def test_follow(self):
        """Авторизованный пользователь может подписываться на других пользователей и удалить подписку"""
        following_user = User.objects.create_user(username='name_following')
        # проверяем, что нет подписки
        self.assertFalse(Follow.objects.filter(user=PostsPagesTests.user, author=following_user).exists())
        # проверяем, что работает потс-запрос к странице follow, создали подписку
        response = self.authorized_client.post(reverse('posts:profile_follow', kwargs={'username': 'name_following'}))
        self.assertEqual(response.status_code, 200)
        # проверяем, что используется соответствующий шаблон
        self.assertTemplateUsed(response, 'posts/follow.html')
        # проверяем, что подписка есть
        self.assertTrue(Follow.objects.filter(user=PostsPagesTests.user, author=following_user).exists())
        # проверяем контекст profile_follow
        author = response.context.get('author')
        self.assertEqual('name_following', author.username)
        # проверяем, что работает пост-запрос к странице unfollow и подписка удалена
        response_unfollow = self.authorized_client.post(reverse('posts:profile_unfollow', kwargs={'username': 'name_following'}))
        self.assertEqual(response_unfollow.status_code, 200)
        # проверяем, что на странице unfollow используется соответствующий шаблон
        self.assertTemplateUsed(response_unfollow, 'posts/unfollow.html')
        # проверяем, что подписка удалена
        self.assertFalse(Follow.objects.filter(user=PostsPagesTests.user, author=following_user).exists())
        # проверяем контекст profile_unfollow
        author_unfollow = response.context.get('author')
        self.assertEqual('name_following', author_unfollow.username)

    def test_follow_index(self):
        """Новая запись пользователя появляется в ленте тех, кто на него подписан и не появляется в ленте тех, кто не подписан."""
        following_user = User.objects.create_user(username='name_following')
        user_not_follow = User.objects.create_user(username='name_not_follow')
        authorized_client_2 = Client()
        authorized_client_2.force_login(user_not_follow)
        # создаем подписку
        self.authorized_client.post(reverse('posts:profile_follow', kwargs={'username': 'name_following'}))
        Post.objects.create(author=following_user,
                            text='Test follow')
        self.assertTrue(Post.objects.filter(author=following_user))
        response = self.authorized_client.get(reverse('posts:follow_index'))
        post_list = response.context.get('page_obj')
        self.assertQuerysetEqual(post_list, Post.objects.filter(author=following_user).order_by('-created')[:10], transform=lambda x: x)
        # у пользователя без подписок нет постов на странице follow_index
        response_2 = authorized_client_2.get(reverse('posts:follow_index'))
        self.assertEqual(len(response_2.context.get("page_obj").object_list), 0)




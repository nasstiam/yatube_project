# posts/tests/test_urls.py
# class StaticURLTests(TestCase):
#     def test_homepage(self):
#         # Создаем экземпляр клиента
#         guest_client = Client()
#         # Делаем запрос к главной странице и проверяем статус
#         response = guest_client.get('/')
#         # Утверждаем, что для прохождения теста код должен быть равен 200
#         self.assertEqual(response.status_code, 200)


from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()

class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='name')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост пост',
        )
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        # self.user = User.objects.create_user(username='noname')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_posts.html': f'/group/{PostsURLTests.group.slug}/',
            'posts/profile.html': f'/profile/{PostsURLTests.user.username}/',
            'posts/post_detail.html': f'/posts/{PostsURLTests.post.id}/'
        }
        # для неавторизованное пользователя
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response_auth = self.guest_client.get(address)
                self.assertTemplateUsed(response_auth, template)
                response_unauth = self.authorized_client.get(address)
                self.assertTemplateUsed(response_unauth, template)

    def test_unexisting_page(self):
        """Запрос к несуществующей странице возвращает ошибку 404"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_create_authorized(self):
        """Запрос к странице Новая запись для авторизованного пользователя"""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_create_unauthorized(self):
        """Запрос к странице Новая запись для неавторизованного пользователя перенаправит на страницу login"""
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/new/')
        # реализовано по-другому в шаблоке через if else для разных статусов пользователей показаны разные возможности
        # как протестировать?!

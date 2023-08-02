from django.test import TestCase, Client
from django.urls import reverse

class StaticURLTests(TestCase):
    guest_client = Client()
    def test_about_author(self):
        """URL-адрес использует соответствующий шаблон about/author"""
        response = StaticURLTests.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech(self):
        """URL-адрес использует соответствующий шаблон about/tech"""
        response = StaticURLTests.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_author_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about/author, доступен."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)

    def test_about_author_page_uses_correct_template(self):
        """При запросе к about:author применяется шаблон about/author.html."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_tech_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about/tech, доступен."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)

    def test_about_tech_page_uses_correct_template(self):
        """При запросе к about:tech применяется шаблон about/techr.html."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')
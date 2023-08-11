from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        '''nonexist-page: статус ответа сервера - 404, используется шаблон core/404.html'''
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')

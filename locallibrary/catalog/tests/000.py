from unittest import TestCase

from django.contrib.auth.models import User, Permission
from django.urls import reverse

from locallibrary.catalog.models import Author

# создали двух пользователей 1 авт 2 нет
# создали тестового автора
# если не залогинен то открыть страницу регистрации
# Проверка что пользователь залогинился
# Проверка того, что мы используем правильный шаблон
#
#
#
#

class AuthorCreateTest(TestCase):

    def setUp(self):
        # Создание пользователя
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        #Создание автора
        test_author = Author.objects.create(first_name='John',last_name='Smith', Date_of_birth='1970-01-01', Date_of_death='1999-01-01',)
        test_author.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('author_create'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/author/create/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('author_create'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'catalog/author_form.html')

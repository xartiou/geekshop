from django.conf import settings
from django.test import TestCase

from authapp.models import User
from mainapp.models import ProductCategory, Product
from django.test.client import Client


# Create your tests here.

class UserTestCase(TestCase):
    # данные для админа
    username = 'django'
    email = 'dj@mail.ru'
    password = 'geekbrains'

    # данные для теста
    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django1',
        'email': 'django1@mail.ru',
        'password1': 'Geekshop1231_',
        'password2': 'Geekshop1231_',
        'age': 31,
    }

    def setUp(self) -> None:
        # создаем суперюзера
        self.user = User.objects.create_superuser(self.username,self.email,self.password)
        self.client = Client()


    # тест на авторизацию
    def test_login(self):
        # заходим на главную
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # проверяем на неавторизованность
        self.assertTrue(response.context['user'].is_anonymous)
        # пробуем авторизоваться
        self.client.login(username=self.username,password=self.password)
        # переходим на страницу авторизации
        response = self.client.get('/users/login/')

        self.assertEqual(response.status_code, 302)

    # тест на регистрацию
    def test_register(self):
        # заходим на страницу регистрации и передаем данные из словаря выше new_user_data
        response = self.client.post('/users/register/',data=self.new_user_data)
        print(response.status_code)  # проверим код
        #  перенаправляет на страницу авторизации
        self.assertEqual(response.status_code, 302)
        # пытаемся получить usera только что созданного
        user = User.objects.get(username=self.new_user_data['username'])
        # ссылка активации usera только что созданного
        # verify / < str: email > / < str: activate_key > /
        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{user.email}/{user.activation_key}/"
        # пытаемся активироваться
        response = self.client.get(activation_url)

        self.assertEqual(response.status_code,302)
        self.assertFalse(user.is_active)
        # обновляем usera только что созданного в БД
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    # здесь мы закрываем тестирование
    def tearDown(self) -> None:
        pass

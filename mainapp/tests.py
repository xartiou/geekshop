from django.test import TestCase
from mainapp.models import Product, ProductCategory
from django.test.client import Client
# Create your tests here.



class TestMainSmokeTest(TestCase):

    # инициализируем данные для теста
    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='Test')
        Product.objects.create(category=category,name='product_1',price=100)

        # помогает делать запрос
        self.client = Client()

    # тестируем работоспособность сайта
    def test_product_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    # тестируем страницы с детализацией товара
    def test_product_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, 200)

    # здесь мы закрываем тестирование
    def tearDown(self) -> None:
        pass

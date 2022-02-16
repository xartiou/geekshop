from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        # выбираем категорию "Обувь" или продукт с id=4
        #products = Product.objects.filter(Q(category__name='Обувь') | Q(id=4))

        # выбираем категорию "Обувь" и продукт с id=5
        # products = Product.objects.filter(Q(category__name='Обувь') & Q(id=5))

        # выбираем категорию не"Обувь"
        #products = Product.objects.filter(~Q(category__name='Обувь'))

        # выбираем категорию не"Обувь"  продукт с id=14
        products = Product.objects.filter(~Q(category__name='Обувь'), id=14)
        print(products)
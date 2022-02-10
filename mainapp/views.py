import os
from django.views.decorators.cache import cache_page, never_cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView
from django.conf import settings
from django.core.cache import cache
from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.

def index(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)

# функция для кеширования categories
def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()

# функция кеширования всех продуктов
def get_products():
    if settings.LOW_CACHE:
        key = 'link_products'
        link_products = cache.get(key)
        if link_products is None:
            link_products = Product.objects.all().select_related('category')
            cache.set(key, link_products)
        return link_products
    else:
        return Product.objects.all().select_related('category')

# функция кеширования одного продукта
def get_product_one(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


@cache_page(3600)  # кешируем данные страницы
def products(request, id_category=None, page=1):
    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category:
        products = Product.objects.filter(category_id=id_category).select_related('category')
    else:
        products = Product.objects.all().select_related()
        # products = Product.objects.all().prefetch_related() для связи many-to-many
    #products = get_products()  # для кеширования
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    context['categories'] = ProductCategory.objects.all()  # вызов не кешированный
    # context['categories'] = get_link_category()  # вызов кешированный
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # product = self.get_object()  # если не кешируем
        context['product'] = get_product_one(self.kwargs.get('pk'))
        return context

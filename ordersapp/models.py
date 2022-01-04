from django.conf import settings
from django.db import models

from mainapp.models import Product


# Create your models here.

class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCESED = 'STP'
    PAID = 'PD'
    PROCESED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    # выбор статуса заказа
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCESED, 'отправлен на обработку'),
        (PAID, 'оплачено'),
        (PROCESED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отмена заказа'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='обновлён', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    # как будет выглядеть
    def __str__(self):
        return f'Текущий заказ {self.pk}'

    # получаем общее количество
    def get_total_quantity(self):
        items = self.orderitems.select_related('product')  # вытягиваем все связи конкретно по продукту
        return sum(list(map(lambda x: x.quantity, items)))

    # получаем общую стоимость
    def get_total_cost(self):
        items = self.orderitems.select_related('product')  # вытягиваем все связи конкретно по продукту
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    # получаем
    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        pass


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

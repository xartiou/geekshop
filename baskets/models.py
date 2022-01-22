from django.db import models


# Create your models here.
from authapp.models import User
from mainapp.models import Product

# менеджер для метода удаления при работе с QuerySet
class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)



class Basket(models.Model):
    # прописываем менеджер QuerySet в класс
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    # @property
    # def get_baskets(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return baskets

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    # метод удаления при занесении товара в корзину
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete(*args, **kwargs)
    #
    # # метод сохранения при удалении со склада
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         get_item = self.get_item(int(self.pk))
    #         self.product.quantity -= self.quantity - get_item
    #     else:
    #         self.product.quantity -= self.quantity
    #
    #     self.product.save()
    #     super(Basket, self).save(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity

    @staticmethod
    def get_product(user,product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_item = cls.get_item(user)
        basket_item_dic = {}
        [basket_item_dic.update({item.product: item.quantity}) for item in basket_item]
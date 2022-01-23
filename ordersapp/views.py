from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView

from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from mainapp.models import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your views here.


# список заказов(Order)
class OrderListView(ListView, BaseClassContextMixin):  # добавили Mixin чтобы не переопределять title
    model = Order
    title = 'Geekshop | Список заказов'

    def get_queryset(self):  # при удалении будут сохранятся только активные
        return Order.objects.filter(is_active=True, user=self.request.user)


class OrderCreateView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)

        # inlineformset_factory - фабрика форм
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=basket_item.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                # basket_item.delete()
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            Basket.objects.filter(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop | Просмотр заказа'


class OrderUpdateView(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Редактирование заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:  # добавляем пустую форму
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Удаление заказа'


#  функция для смены статусов заказа
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = order.SEND_TO_PROCESED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


    # сигнал функция обновления количества товаров или корзины при Сохранении в заказ
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:  # если создан
        get_item = instance.get_item(int(instance.pk))
        instance.product.quantity -= instance.quantity - get_item
    else: # если не создан(новый)
        instance.product.quantity -= instance.quantity
    instance.product.save()

    # сигнал функция обновления количества товаров или корзины при Удалении заказа
@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete,sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


# контроллер получения цены продукта если есть pk, если нет то 0
# def product_price(request,pk):
#     if request.is_ajax():
#         product_item = Product.objects.filter(pk=pk).first()
#         if product_item:
#             return JsonResponse({'price': product_item.price})
#         return JsonResponse({'price': 0})

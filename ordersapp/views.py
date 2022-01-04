from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView

from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


# Create your views here.


# список заказов(Order)
class OrderListView(ListView, BaseClassContextMixin):  # добавили Mixin чтобы не переопределять title
    model = Order
    title = 'Geekshop | Список заказов'

    def get_queryset(self):
        return Order.objects.filter(is_active=True)  # при удалении будут сохранятся только активные


class OrderCreateView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')
    title = 'Geekshop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)

        # inlineformset_factory - фабрика форм
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=basket_item.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                basket_item.delete()
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
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
    pass


class OrderDeleteView(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'Geekshop | Удаление заказа'


#  функция для смены статусов заказа
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = order.SEND_TO_PROCESED
    order.save()
    return HttpResponseRedirect(reverse('order:list'))

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from mainapp.mixin import BaseClassContextMixin
from ordersapp.models import Order


# Create your views here.


# список заказов(Order)
class OrderListView(ListView, BaseClassContextMixin):  # добавили Mixin чтобы не переопределять title
    model = Order
    title = 'Geekshop | Список заказов'


class OrderCreateView(CreateView):
    pass


class OrderDetailView(DetailView):
    pass


class OrderUpdateView(UpdateView):
    pass


class OrderDeleteView(DeleteView):
    pass


#  функция для смены статусов заказа
def order_forming_complete(request, pk):
    pass

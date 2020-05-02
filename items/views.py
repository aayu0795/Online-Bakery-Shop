from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Item
from cart.models import OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin


def check_item_in_cart(request, item):
    try:
        order_qs = Order.objects.filter(user=request.user)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(item=item)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                if order_item in order.items.all():
                    return True
        # if book not present in cart
        return False
    except TypeError:
        return False

# /


class HomepageView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'items/index.html'


# /slug:slug>/
class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'items/category.html'


# /<slug:category_slug>/<slug:slug>/
class ItemDetailView(LoginRequiredMixin, DetailView):
    lofin_url = 'accounts/login/'
    model = Item
    context_object_name = 'item'
    template_name = 'items/item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if check_item_in_cart(self.request, context['item']):
            context.update({'in_cart': True})
        return context

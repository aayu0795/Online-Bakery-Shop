from .models import Category, Item
from django.shortcuts import render
from cart.models import OrderItem, Order
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


def check_item_in_cart(request, item):
    '''
    This view identify if item present in 
    cart for logged in user or not
    '''
    try:
        order_qs = Order.objects.filter(user=request.user)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(item=item)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                if order_item in order.items.all():
                    return True
        # if item not present in cart
        return False
    except TypeError:
        return False


class HomepageView(ListView):
    '''
    It's the homepage view of website
    '''
    model = Category
    context_object_name = 'categories'
    template_name = 'items/index.html'


class CategoryDetailView(DetailView):
    '''
    This view lists out all the categories 
    '''
    model = Category
    context_object_name = 'category'
    template_name = 'items/category.html'


class ItemDetailView(LoginRequiredMixin, DetailView):
    '''
    This view provide the complete details of the
    instance item
    '''
    lofin_url = 'accounts/login/'
    model = Item
    context_object_name = 'item'
    template_name = 'items/item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if check_item_in_cart(self.request, context['item']):
            context.update({'in_cart': True})
        return context

from django.urls import path
from .views import add_to_cart, remove_from_cart, order_view, checkout

app_name = 'cart'

urlpatterns = [
    path('order_summary/', order_view, name='order-summary'),
    path('add_to_cart/<slug:item_slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug:item_slug>/',
         remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout, name='checkout'),
]

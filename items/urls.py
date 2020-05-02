from django.urls import path
from .views import HomepageView, CategoryDetailView, ItemDetailView


app_name = 'items'

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:slug>/',
         ItemDetailView.as_view(), name='item'),
]

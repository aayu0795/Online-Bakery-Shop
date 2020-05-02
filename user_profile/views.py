from django.shortcuts import render, redirect
from .models import User_orders
from datetime import datetime
from .forms import Category_form, Item_form
from django.contrib import messages


def profile_view(request):
    now = datetime.now()
    orders = User_orders.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'now': now
    }
    return render(request, 'user_profile/profile.html', context)


def admin_view(request):
    new_category = Category_form(request.POST or None)
    if new_category.is_valid():
        new_category.save()
        messages.success(request, "New category was created successfully!")
        return redirect('/accounts/admin/')

    now = datetime.now()
    orders = User_orders.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'now': now,
        'category_form': Category_form(),
        'item_form': Item_form()
    }
    return render(request, 'user_profile/admin.html', context)


def create_item_via_admin(request):
    new_item = Item_form(request.POST or None, request.FILES)
    if new_item.is_valid():
        new_item.save()
        messages.success(request, "New item was created successfully!")
        return redirect('/accounts/admin/')

    messages.error(
        request, f"Error occoured while creating the item! {new_item.errors.as_data()}")
    return redirect('/accounts/admin/')

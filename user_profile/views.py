from datetime import datetime
from .models import User_orders
from django.contrib import messages
from .forms import Category_form, Item_form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    '''
    This is the register user profile view
    it includes user details and all previous orders
    '''
    now = datetime.now()    # current date and time
    orders = User_orders.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'now': now
    }
    return render(request, 'user_profile/profile.html', context)


@login_required
def admin_view(request):
    '''
    If the logged in user is super user/admin
    this view allow user to preform CRUD operations
    '''
    new_category = Category_form(request.POST or None)  # if method == 'POST'
    if new_category.is_valid():
        new_category.save()
        messages.success(request, "New category was created successfully!")
        return redirect('/accounts/admin/')

    now = datetime.now()    # current date and time
    orders = User_orders.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'now': now,
        'category_form': Category_form(),
        'item_form': Item_form()
    }
    return render(request, 'user_profile/admin.html', context)


@login_required
def create_item_via_admin(request):
    '''
    This view allow user to create new item of any category
    '''
    new_item = Item_form(request.POST or None, request.FILES)
    if new_item.is_valid():
        new_item.save()
        messages.success(request, "New item was created successfully!")
        return redirect('/accounts/admin/')

    messages.error(
        request, f"Error occoured while creating the item! {new_item.errors.as_data()}")
    return redirect('/accounts/admin/')

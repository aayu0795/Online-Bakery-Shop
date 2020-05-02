from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Order, OrderItem, Payment
import string
import random
from items.models import Item
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from user_profile.models import User_orders
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))


def send_email(instance):
    to = [instance.user.email]
    subject = "Order Confirmation"
    sender = settings.EMAIL_HOST_USER
    template_name = 'user_profile/order_confirmation.html'
    context = {'order': instance}

    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html,
                       from_email=sender, to=to)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()


@login_required
def add_to_cart(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    order_item, created = OrderItem.objects.get_or_create(item=item)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    order_item = get_object_or_404(OrderItem, item=item)
    order = Order.objects.get(user=request.user)
    order.items.remove(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def order_view(request):
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        context = {
            'order': order_qs[0]
        }
        return render(request, "cart/order_summary.html", context)

    context = {
        'order': None
    }
    return render(request, "cart/order_summary.html", context)


@login_required
def checkout(request):
    order_qs = Order.objects.filter(user=request.user)

    if order_qs.exists():
        order = order_qs[0]
    else:
        return Http404

    if request.method == 'POST':
        try:
            # complete the order (`ref code` and set ordered to true)
            order.ref_code = create_ref_code()
            token = request.POST.get('stripeToken')

            # create a stripe charge
            charge = stripe.Charge.create(
                amount=int(order.get_total()),
                currency="inr",
                source=token,
                description=f'charge for {request.user.username}',
            )

            # create a payment objects and link to order
            payment = Payment()
            payment.order = order
            payment.stripe_charge_id = charge.id
            payment.total = order.get_total()
            payment.save()

            # complete the order (ref code)
            order.save()

            # Add order details to user orders
            new_order = User_orders.objects.create(
                user=request.user,
                order_ref_code=order.ref_code,
                order_total=order.get_total()
            )

            for item in order.items.all():
                new_order.order_items.add(item)

            new_order.save()

            # send order confrmation via email
            send_email(new_order)

            # delete from cart
            order.delete()

            # redirect to the user's profile
            return redirect('/accounts/profile/')

        # send email for all the errors

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(request, "There was card error.")
            return redirect(reverse("cart:checkout"))

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "There was Rate limit error on stripe.")
            return redirect(reverse("cart:checkout"))

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid parameters for stripe request.")
            return redirect(reverse("cart:checkout"))

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Invalid stripe API key.")
            return redirect(reverse("cart:checkout"))

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(
                request, "There was a network error. Please try again.")
            return redirect(reverse("cart:checkout"))

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "There was a error. Please try again.")
            return redirect(reverse("cart:checkout"))

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            print("ERROR DURING CHECKOUT", e)
            messages.error(
                request, "There was Serious error. We are trying to resolve the issue.")
            return redirect(reverse("cart:checkout"))

    context = {
        'order': order
    }
    return render(request, 'cart/checkout.html', context)

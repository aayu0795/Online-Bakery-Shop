from django.db import models
from items.models import Item
from django.conf import settings
from django.db.models import Sum


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    # def get_total(self):
    #     return self.items.all().aggregate(order_total=Sum('item__price'))['order_total']

    def get_total(self):
        total = 0.0
        for item in self.items.all():
            total += item.item.get_price
        return total


class Payment(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    total = models.FloatField()
    date_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id

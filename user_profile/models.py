from django.db import models
from django.conf import settings
from cart.models import OrderItem


class User_orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    order_ref_code = models.CharField(max_length=50)
    order_total = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User order's"
        ordering = ['-order_date']

    def __str__(self):
        return self.user.username

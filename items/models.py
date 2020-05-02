from django.db import models
from django.shortcuts import reverse


CATEGORY_CHOICES = {
    ('Bread', 'Bread'),
    ('Brownies', 'Brownies'),
    ('Cakes', 'Cakes'),
    ('Drinks', 'Drinks'),
    ('Fruit Pies', 'Fruit Pies'),
    ('Pasteries', 'Pasteries')
}


class Category(models.Model):
    title = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:category', kwargs={
            'slug': self.slug
        })

    @property
    def get_top_three_items(self):
        return self.item_set.all()[:3]


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    price = models.FloatField()
    thumbnail = models.ImageField()
    offer = models.BooleanField(default=False)
    slug = models.SlugField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:item', kwargs={
            'category_slug': self.category.slug,
            'slug': self.slug
        })

    @property
    def get_discount(self):
        if self.offer == True:
            discounted_value = self.price - \
                ((self.price * self.discount.discount_value) / 100)
            return discounted_value
        return False

    @property
    def get_price(self):
        if self.offer == True:
            discounted_value = self.price - \
                ((self.price * self.discount.discount_value) / 100)
            return discounted_value
        return self.price


class Discount(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    discount_value = models.IntegerField()

    def __str__(self):
        return f'{self.item.title}, {self.discount_value}%'

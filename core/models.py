from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICE = (
    ('S', 'Shirt'),
    ('SP', 'Sports'),
    ('W', 'Winter'),
    ('P', 'Party Wear'),
    ('F', 'Formals'),
    ('C', 'Casuals'),
    ('B', 'Bikini'),
)

Label_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

""" All the Items available for shopping """
class Item(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(default="default.jpg")
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2)
    label = models.CharField(choices=Label_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField(default="This is a Fake Description")
    bestseller = models.BooleanField(default=False)
    isNewItem = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

""" Items which are being ordered"""
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

""" All ordered Items together like a shopping cart"""
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
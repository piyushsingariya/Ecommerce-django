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
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

""" Items which are being ordered"""
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_price(self):
        if not self.item.discount_price:
            return self.quantity * self.item.price
        else:
            return self.quantity * self.item.discount_price
    def get_total_savings(self):
        return self.quantity * (self.item.price - self.item.discount_price)


""" All ordered Items together like a shopping cart"""
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def get_final_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total
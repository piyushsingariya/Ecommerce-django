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


"""All ordered Items together like a shopping cart"""
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=30, default=0)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)


    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
    def get_final_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    def __str__(self):
        return self.code


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stripe_charge_id
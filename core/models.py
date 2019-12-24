from django.conf import settings
from django.db import models

""" All the Items available for shopping """
class Item(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField()

    def __str__(self):
        return self.title

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
from django.shortcuts import render
from .models import Item


def index(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "index.html", context)

def products(request):
    return render(request, "products.html", {})

def checkout(request):
    return render(request, "checkout.html", {})
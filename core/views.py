from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

class IndexView(ListView):
    model = Item
    template_name = "index.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def checkout(request):
    return render(request, "checkout.html", {})
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages

class IndexView(ListView):
    model = Item
    paginate_by = 4
    template_name = "index.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item quantity has been updated to your Cart")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This Item has been added to your Cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item has been added to your Cart")
    return redirect("core:product", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This Item has been removed to your Cart")
            return redirect("core:product", slug=slug)
        else:
            # Add a message that order doesn't not contain the order item
            messages.info(request, "This Item isn't in your Cart")
            return redirect("core:product", slug=slug)
    else:
        # Add a message that user doesn't have an order
        messages.info(request, "You do not have an active order!!!")
        return redirect("core:product", slug=slug)

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def checkout(request):
    return render(request, "checkout.html", {})
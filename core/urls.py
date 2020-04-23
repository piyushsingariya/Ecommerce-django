from django.urls import path, include
from .views import (ItemDetailView,
                    checkout,
                    IndexView,
                    add_to_cart,
                    remove_from_cart,
                    OrderSummaryView,
                    remove_single_item_from_cart,
                    add_single_item_to_cart)

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('checkout/', checkout, name="checkout-page"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('add-single-item-to-cart/<slug>', add_single_item_to_cart, name="add-single-item-to-cart"),

]
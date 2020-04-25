from django.urls import path, include
from .views import (ItemDetailView,
                    CheckoutView,
                    IndexView,
                    add_to_cart,
                    remove_from_cart,
                    OrderSummaryView,
                    remove_single_item_from_cart,
                    add_single_item_to_cart,
                    PaymentView,
                    AddCouponView,
                    RequestRefundView)

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('checkout/', CheckoutView.as_view(), name="checkout-page"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('add-single-item-to-cart/<slug>', add_single_item_to_cart, name="add-single-item-to-cart"),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('add-coupon/', AddCouponView.as_view(), name="add-coupon"),
    path('request-refund/', RequestRefundView.as_view(), name="request-refund"),
]
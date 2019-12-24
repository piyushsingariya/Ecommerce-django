from django.urls import path, include
from .views import index, products, checkout

app_name = 'core'
urlpatterns = [
    path('', index, name="index"),
    path('products/', products, name="product-list"),
    path('checkout/', checkout, name="checkout-page")
]
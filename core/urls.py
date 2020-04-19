from django.urls import path, include
from .views import ItemDetailView, products, checkout, IndexView

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('checkout/', checkout, name="checkout-page")
]
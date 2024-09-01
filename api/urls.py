from api import views
from django.urls import path

urlpatterns = [
    path("products/", views.get_all_products, name='api_products'),
    path("products/add_product_to_cart/", views.add_product_to_cart, name='api_add_product_to_cart'),
]

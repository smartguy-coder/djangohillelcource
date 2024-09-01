from api import views
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    path("products/", views.get_all_products, name='api_products'),
    path("products/add_product_to_cart/", views.add_product_to_cart, name='api_add_product_to_cart'),
    path('', include(router.urls)),
]

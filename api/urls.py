from api import views
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, \
    AllCartsAPIView

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    # path("products/", views.get_all_products, name='api_products'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('cart/', AllCartsAPIView.as_view(), name='all_carts'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path("products/add_product_to_cart/", views.add_product_to_cart, name='api_add_product_to_cart'),
    path('', include(router.urls)),
]

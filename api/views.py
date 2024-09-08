from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from retail.models import Product, Cart, CartItem

from rest_framework import viewsets, generics
from retail.models import ProductCategory
from retail.serializers import ProductCategorySerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def get_all_products(request):
    products = Product.objects.select_related(
        'producer'
    ).prefetch_related(
        'category'
    ).all()
    products_serialized = [
        {
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'description': p.description,
            'producer': p.producer.name,
            'categories': [c.title for c in p.category.all()]
        }
        for p in products
    ]
    return JsonResponse({'products': products_serialized})


@require_POST
@csrf_exempt
def add_product_to_cart(request):
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=user, is_closed=False)
    cart_item, created_item = CartItem.objects.get_or_create(cart=cart, product=product)
    if created_item and quantity > 1:
        cart_item.quantity += quantity - 1  # default is 1
    else:
        cart_item.quantity += quantity
    cart_item.save()

    return JsonResponse({'cart_id': cart.id})
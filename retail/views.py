import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F


from retail.models import Product, Cart, CartItem

stripe.api_key = settings.STRIPE_KEY
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# @cache_page(60 * 15)
def index(request):
    products = Product.objects.select_related(
        'producer'
    ).prefetch_related(
        'category'
    ).all()
    result = cache.get('my_key')

    if result is None:
        # Якщо результат не в кеші, обчислюємо його і кешуємо
        result = 'calculated data'
        print('chache was used')
        cache.set('my_key', result, 60 * 15)

    return render(request, 'index.html', {'products': products})


@login_required
def cart_detail(request):

    cart = Cart.objects.filter(user=request.user, is_closed=False).first()
    if cart:
        items = cart.items.select_related('product').all()
        total_cost = items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
        total_cost = round(total_cost, 2)
    else:
        items = []
        total_cost = 0
    return render(request, 'cart_detail.html', {'cart': cart, 'total_cost': total_cost, 'items': items})


@login_required
def update_cart(request, product_id, action):
    cart, created = Cart.objects.get_or_create(user=request.user, is_closed=False)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if action == 'add':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'remove':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    # Повернутися на ту ж саму сторінку - використовуємо квері параметри в шаблонізаторах
    next_url = request.GET.get('next', reverse('index_page'))
    return HttpResponseRedirect(next_url)


@login_required
@require_POST
def process_stripe_payment(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=request.user, is_closed=False)
    if not cart:
        return reverse('index_page')
    items = cart.items.select_related('product').all()
    if not items:
        return reverse('index_page')
    total_cost = items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    total_cost = round(total_cost, 2)

    line_items: list[dict] = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": cart_product.product.title,
                    "description": cart_product.product.description,
                    "images": [str(cart_product.product.image_url)],
                },
                "unit_amount": int(cart_product.product.price * 100),
            },
            "quantity": cart_product.quantity,
        }
        for cart_product in items
    ]

    session_stripe: dict = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("success_payment")),
        cancel_url=request.build_absolute_uri(reverse("failed_payment")),
        # locale='en',  # uk not supported
        metadata={"user_id": user.id, "total_cost": total_cost, "cart_id": cart.id},
        **({'customer_email': user.email} if user.email else {})
    )
    return HttpResponseRedirect(session_stripe["url"])


def success_payment(request):
    return render(request, 'success_payment.html')


def failed_payment(request):
    return render(request, 'failed_payment.html')


@csrf_exempt
@require_POST
def hook_stripe_payment(request):
    data = json.loads(request.body)
    try:
        event = stripe.Event.construct_from(data, settings.STRIPE_KEY)
    except stripe.error.SignatureVerificationError:
        return

    if event["type"] == "checkout.session.completed":

        user_id = event["data"]["object"]["metadata"]["user_id"]
        cart = Cart.objects.filter(user_id=user_id, is_closed=False).first()
        if cart:
            items = cart.items.select_related('product').all()
            total_cost = items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
            total_cost = round(total_cost, 2)
            print(event)
            if float(event["data"]["object"]["metadata"]["total_cost"]) != float(total_cost):
                raise ValueError(f'Probably user added some products into basket after starting payment process. Call them {user_id=})')
            cart.is_closed = True
            cart.save()
    return JsonResponse({'status': 'OK'})

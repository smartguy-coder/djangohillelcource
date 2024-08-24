from django.urls import path

from retail import views

urlpatterns = [
    path("", views.index, name='index_page'),

    path("cart_detail", views.cart_detail, name='cart_detail'),
    path('cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),

    path('process_stripe_payment', views.process_stripe_payment, name='process_stripe_payment'),
    path('success_payment', views.success_payment, name='success_payment'),
    path('failed_payment', views.failed_payment, name='failed_payment'),
    path('hook_stripe_payment', views.hook_stripe_payment, name='hook_stripe_payment'),

]

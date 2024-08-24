from django.db import models

from django.contrib.auth import get_user_model  # new
UserModel = get_user_model()


class ProductCategory(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Producer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField()
    category = models.ManyToManyField(ProductCategory)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# new
class Cart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

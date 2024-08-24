from django.contrib import admin
from .models import ProductCategory, Producer, Product

admin.site.register(ProductCategory)
admin.site.register(Producer)
admin.site.register(Product)
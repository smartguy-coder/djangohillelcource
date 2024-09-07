from rest_framework import serializers
from .models import ProductCategory, Producer, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=True)
    producer = ProducerSerializer()
    instant_discount = serializers.SerializerMethodField()
    extra_info = serializers.CharField(write_only=True, required=False)  # Поле для запису, але не частина моделі

    def get_instant_discount(self, obj):
        return obj.instant_discount

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        extra_info = validated_data.pop('extra_info', None)  # Отримати значення, якщо воно є
        categories_data = validated_data.pop('category')
        producer_data = validated_data.pop('producer')
        producer, created = Producer.objects.get_or_create(**producer_data)
        product = Product.objects.create(producer=producer, **validated_data)
        for category_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(**category_data)
            product.category.add(category)
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('category')
        producer_data = validated_data.pop('producer')
        producer, created = Producer.objects.get_or_create(**producer_data)
        instance.producer = producer

        # Оновлення продукту
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()

        # Оновлення категорій
        instance.category.clear()
        for category_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(**category_data)
            instance.category.add(category)

        return instance

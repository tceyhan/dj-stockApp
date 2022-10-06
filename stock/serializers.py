from rest_framework import serializers

from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField(write_only=True)
    

    class Meta:
        model = Product
        fields = ('id', "name","category", "category_id",
                  "brand", "brand_id", "stock")
        
        read_only_fields = ('stock',)

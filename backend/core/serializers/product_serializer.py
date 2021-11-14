from rest_framework import serializers
from core.models import Product, Product_Shop, ProductReview, OrderProduct
from .shop_serializer import ShopSerializer
from django.db.models import Q


# To be changed for Product_Shop


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category(self, obj):
        return obj.get_categories_name()


class ProductShopSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart_value = serializers.SerializerMethodField()

    class Meta:
        model = Product_Shop
        fields = ('product', 'seller_price', 'slug', 'cart_value')

    def get_cart_value(self, obj):
        user = self.context.get("user")
        if(user):
            lookups = Q(user=user) & Q(product=obj) & Q(ordered=False)
            a = OrderProduct.objects.filter(lookups)
            if a.exists():
                return a[0].quantity
            else:
                return 0
        else:
            return None


class SearchProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('name', 'category')

    def get_category(self, obj):
        return obj.get_categories_name()

# class SearchSerializer(serializers.ModelSerializer):

# To be changed for Product_Shop


class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
        # product = Product.objects.create(name=validated_data['name'], description = validated_data['description'], sku = validated_data['sku'], weight = validated_data['weight'], price = validated_data['price'], discounted_price=validated_data['discounted_price'], category=)


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('__all__')

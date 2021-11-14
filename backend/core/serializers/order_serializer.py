from rest_framework import serializers
from accounts.models import BillingAddress
from core.models import Order, OrderProduct
from .product_serializer import ProductSerializer, ProductShopSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingAddress
        fields = ('name', 'contact', 'contact2', 'apartment_address', 'street_address', 'area_pincode', 'city', 'state',
                  'address_type', 'default_shipping', 'default_billing', 'slug')

    def create(self, validated_data):
        shipping_address = BillingAddress.objects.create(user=self.context.get("user"), name=validated_data['name'], contact=validated_data['contact'], contact2=validated_data['contact2'], apartment_address=validated_data['apartment_address'], street_address=validated_data[
            'street_address'], area_pincode=validated_data['area_pincode'], state=validated_data['state'], address_type=validated_data['address_type'], city=validated_data['city'], default_shipping=validated_data['default_shipping'], default_billing=validated_data['default_billing'])
        return shipping_address


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductShopSerializer()
    product_total = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = ('ordered', 'quantity', 'product', 'product_total', 'seller_name')

    def get_product_total(self, obj):
        return obj.get_total_seller_product_price()

    def get_seller_name(self, obj):
        return obj.get_seller_name()


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)
    billing_address = ShippingAddressSerializer()
    shipping_address = ShippingAddressSerializer()
    total_products_quantity = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('products', 'start_date', 'ordered_date', 'ordered', 'billing_address', 'shipping_address', 'being_delivered',
                  'received', 'refund_requested', 'refund_granted','total_products_quantity')

    def get_total_products_quantity(self, obj):
        return obj.get_total_products_quantity()
    # def get_category(self, obj):
    #     return obj.get_categories_name()

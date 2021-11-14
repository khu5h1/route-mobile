from rest_framework import serializers
from core.models import Shop, ShopReview

# TODO : products_categories is to be arranged as per manytomanyfields


class ShopSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('name', 'gstin_number', 'longitude', 'latitude', 'contact', 'contact2', 'address', 'street', 'city', 'area_pincode', 'state', 'description',
                  'products_categories', 'category', 'rating', 'open_time', 'close_time', 'closed_days', 'slug', 'image')

    def create(self, validated_data):
        shop = Shop.objects.create(business=self.context.get("business"), name=validated_data['name'], gstin_number=validated_data['gstin_number'],
                                   longitude=validated_data['longitude'], latitude=validated_data[
                                       'latitude'], contact=validated_data['contact'], contact2=validated_data['contact2'],
                                   address=validated_data['address'], street=validated_data[
                                       'street'], city=validated_data['city'],
                                   area_pincode=validated_data['area_pincode'], state=validated_data[
                                       'state'], description=validated_data['description'],
                                   products_categories=validated_data[
                                       'products_categories'], rating=validated_data['rating'],
                                   open_time=validated_data['open_time'], close_time=validated_data['close_time'], closed_days=validated_data['closed_days'])
        return shop

    def get_category(self, obj):
        return obj.get_categories_name()


class ShopSerializerForLeftPane(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('name', 'address', 'street', 'city', 'area_pincode',
                  'category', 'rating', 'open_time', 'close_time', 'image')

    def get_category(self, obj):
        return obj.get_categories_name()

        # for status of shop, it will be figured on frontend using javascript


class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = '__all__'

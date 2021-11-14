from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.serializers import ShopSerializer, ShopSerializerForLeftPane, ProductSerializer, ShopReviewSerializer
from core.models import Shop, Product, ShopReview
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from accounts.models import BusinessAccount
from backend.pagination import CustomPagination

# TODO manage pagination
# For the owner to be able to view/add shops to his business acc


class AllShopsViewAPI(generics.ListAPIView):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    pagination_class = None


class BusinessShopViewAPI(generics.GenericAPIView):
    pagination_class = CustomPagination
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        data = []
        shops = Shop.objects.filter(business__user=request.user)
        page = self.paginate_queryset(shops)
        if page is not None:
            serializer = self.get_serializer(shops, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(shops, many=True)
            data = serializer.data
        return Response(data)

    def post(self, request, *args, **kwargs):
        if request.GET['query'] == 'add':
            business = BusinessAccount.objects.get(user=request.user)
            context = {"business": business}
            serializer = self.get_serializer(
                data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "detail": "Shop Added Successfully",
            }, status=status.HTTP_200_OK)

        # TODO This is to be done by Serializer

        if request.GET['query'] == 'update':
            shop_id = request.data['shop_id']
            shop = Shop.objects.get(pk=shop_id)
            valid_data = {}
            request_fields = request.data.keys()

            if('name' in request_fields):
                shop.name = request.data['name']
                valid_data['name'] = request.data['name']

            if('contact' in request_fields):
                shop.contact = request.data['contact']
                valid_data['contact'] = request.data['contact']

            if('contact2' in request_fields):
                shop.contact2 = request.data['contact2']
                valid_data['contact2'] = request.data['contact2']

            if('description' in request_fields):
                shop.description = request.data['description']
                valid_data['description'] = request.data['description']

            if('products_categories' in request_fields):
                shop.products_categories = request.data['products_categories']
                valid_data['products_categories'] = request.data['products_categories']

            try:
                shop.save()
                data = {'detail': 'Details Updated Successfully'}
            except:
                data = {'detail': 'Please provide valid values'}
            # serializer = self.get_serializer(shop, data=valid_data)
            # serializer.is_valid(raise_exception=True)
            # self.perform_update(serializer)
            return Response(data)


class ShopViewAPI(generics.GenericAPIView):
    serializer_class = ShopSerializerForLeftPane
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        if kwargs['slug']:
            # TODO add check for same shop user here
            data = []
            shop = get_object_or_404(Shop, slug=kwargs['slug'])
            serializer = self.get_serializer(shop)
            data = serializer.data
            return Response(data)
        elif request.get('pincode'):
            shops = Shop.objects.filter(area_pincode=request.get('pincode'))
            page = self.paginate_queryset(shops)
            if page is not None:
                serializer = self.get_serializer(shops, many=True)
                result = self.get_paginated_response(serializer.data)
                data = result.data
            else:
                serializer = self.get_serializer(shops, many=True)
                data = serializer.data
            return Response(data)
        else:
            return Response({"message": "Please Provide a Shop"}, status=status.HTTP_400_BAD_REQUEST)


class ShopRatingViewAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO add check for same shop user here

        query = kwargs['slug']
        if query is not None:
            shop = get_object_or_404(Shop, slug=query)
            rating = shop.rating
            return Response({
                "rating": rating,
            })
        else:
            message = "Please select a valid shop"
            return Response({
                "detail": message
            }, status=status.HTTP_404_NOT_FOUND)


class ShopReviewsAPI(generics.GenericAPIView):
    serializer_class = ShopReviewSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        # TODO add check for same shop user here

        query = kwargs['slug']
        if query is not None:
            shopReview = ShopReview.objects.filter(shop__slug=query).order_by(
                '-date').exclude(review__isnull=True).exclude(review__exact='')
            page = self.paginate_queryset(shopReview)
            if page is not None:
                serializer = self.get_serializer(shopReview, many=True)
                result = self.get_paginated_response(serializer.data)
                reviews = result.data
            else:
                serializer = self.get_serializer(shopReview, many=True)
                reviews = serializer.data
            return Response(reviews)
        else:
            message = "Please select a valid shop"
            return Response({
                "detail": message
            })


class ExploreProductsAPI(generics.GenericAPIView):
    pagination_class = CustomPagination
    serializer_class = ProductSerializer

    def get(self, requst, *args, **kwargs):
        # TODO add check for same shop user here

        query = kwargs['slug']
        if query is not None:
            shop = get_object_or_404(Shop, slug=query)
            prod_qs = shop.get_products()
            page = self.paginate_queryset(prod_qs)
            if page is not None:
                serializer = self.get_serializer(prod_qs, many=True)
                result = self.get_paginated_response(serializer.data)
                products = result.data
            else:
                serializer = self.get_serializer(prod_qs, many=True)
                products = serializer.data
            return Response(products)
        else:
            message = "Please select a valid product"
            return Response({
                "detail": message
            })

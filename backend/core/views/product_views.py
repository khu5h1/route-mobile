from accounts.models import ADDRESS_CHOICES, RegularAccount
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.response import Response
from core.models import Product, ProductReview, Product_Shop
from rest_framework import status
from django.db.models import Q
from backend.pagination import CustomPagination
from core.serializers import ProductSerializer, ProductReviewSerializer, SearchProductSerializer, ProductShopSerializer
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ProductSearchApi(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = SearchProductSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get('keyword')

        if query is not None:
            lookups = Q(name__icontains=query) | Q(
                description__icontains=query) | Q(other_details__icontains=query) | Q(category__name__icontains=query)
            results = Product.objects.filter(lookups).distinct()
            page = self.paginate_queryset(results)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                result = self.get_paginated_response(serializer.data)
                data = result.data  # pagination data
            else:
                serializer = self.get_serializer(results, many=True)
                data = serializer.data
            return Response(data)
        else:
            message = "Please supply a query"
            return Response({
                "detail": message
            })

# TODO maybe use slug for the product


class ProductSearchWithCategoryApi(generics.ListAPIView):
    serializer_class = ProductShopSerializer

    def get(self, request, *args, **kwargs):
        sslug = kwargs['sslug']
        cslug = kwargs['cslug']
        context={"user":False}
        if isinstance(request.user, RegularAccount) :
            context = {"user" : request.user}
        if sslug and cslug:
            lookups = Q(seller__slug=sslug) & Q(product__category__name=cslug)
            results = Product_Shop.objects.filter(lookups)
            serializer = self.get_serializer(results, many=True, context=context)
            data = serializer.data
            return Response(data)
        else:
            return Response({"detail": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
# TODO: to be changed as per product_Shop


class ProductViewAPI(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        # query = request.GET.get('slug')
        query = kwargs['slug']
        if query is not None:
            # TODO add check for same user here and also fetch the data of just logged in user

            prod = get_object_or_404(Product, slug=query)
            if(prod.user == request.user):
                serializer = self.get_serializer(prod)
                product = serializer.data
                return Response(product)
            else:
                message = "Please select a valid product"
                return Response({
                    "detail": message
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            message = "Please select a valid product"
            return Response({
                "detail": message
            }, status=status.HTTP_404_NOT_FOUND)

#  TODO this is not completed and this is yet to be completed


class ProductReviewsAPI(generics.GenericAPIView):
    serializer_class = ProductReviewSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        query = kwargs['slug']
        if query is not None:
            # TODO add check for same user here and also fetch the data of just logged in user
            productReview = ProductReview.objects.filter(product__slug=query).order_by(
                '-date').exclude(review__isnull=True).exclude(review__exact='')
            page = self.paginate_queryset(productReview)
            if page is not None:
                serializer = self.get_serializer(productReview, many=True)
                result = self.get_paginated_response(serializer.data)
                reviews = result.data
            else:
                serializer = self.get_serializer(productReview, many=True)
                reviews = serializer.data
            return Response(reviews)
        else:
            message = "Please select a valid product"
            return Response({
                "detail": message
            })


class ProductRatingViewAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = kwargs['slug']
        if query is not None:
            product = get_object_or_404(Product, slug=query)
            rating = product.rating
            return Response({
                "rating": rating,
            })
        else:
            message = "Please select a valid product"
            return Response({
                "detail": message
            }, status=status.HTTP_404_NOT_FOUND)


class ProductAddApi(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        # context = {"reg_user": reg_user_details, "user": request.user}
        # serializer = self.get_serializer(data=valid_data, context=context)
        if('category' in request.data.keys()):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({
                "detail": "Please provide a category",
            }, status=status.HTTP_400_BAD_REQUEST)

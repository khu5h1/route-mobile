from core.models.product_models import Product, Product_Variant
from typing import OrderedDict
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.response import Response
from core.models import OrderProduct, Order, Product_Shop
from accounts.models import BillingAddress, BusinessAccount, RegularAccount
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from backend.pagination import CustomPagination
from core.serializers import OrderSerializer, ShippingAddressSerializer, OrderProductSerializer
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.utils import timezone

# TODO test basic profiling using dummy values and add values using automated script


class CartEditAPI(generics.GenericAPIView):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        if(kwargs['action'] == 'add'):
            product_shop_slug = request.data.get('pslug', None)
            pquantity = request.data.get('quantity', 1)
            if product_shop_slug is None:
                return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
            product_shop = get_object_or_404(
                Product_Shop, slug=product_shop_slug)
            order_product_qs = OrderProduct.objects.filter(
                user=request.user,
                product=product_shop,
                ordered=False
            )
            if order_product_qs.exists():
                order_product = order_product_qs.first()
                order_product.quantity += pquantity
                order_product.save()
            else:
                order_product = OrderProduct.objects.create(user=request.user,
                                                            ordered=False,
                                                            product=product_shop,
                                                            quantity=pquantity)

            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if not order.products.filter(product__id=order_product.id).exists():
                    order.products.add(order_product)
            else:
                order = Order.objects.create(user=request.user)
                order.products.add(order_product)
            return Response({"quantity": order_product.quantity},status=HTTP_200_OK)
        if(kwargs['action'] == 'remove'):
            product_shop_slug = request.data.get('pslug', None)
            pquantity = request.data.get('quantity', 1)
            if product_shop_slug is None:
                return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
            product_shop = get_object_or_404(
                Product_Shop, slug=product_shop_slug)
            order_product_qs = OrderProduct.objects.filter(
                user=request.user,
                product=product_shop,
                ordered=False
            )
            returnquantity=0

            if order_product_qs.exists():
                order_product = order_product_qs.first()
                if order_product.quantity - pquantity <= 0:
                    order_product.delete()
                else:
                    order_product.quantity -= pquantity
                    order_product.save()
                    returnquantity= order_product.quantity
                order = Order.objects.get(user=request.user, ordered=False)
                if order.products.all().count() <= 0:
                    order.delete()
            else:
                return Response({"message": "Product is not in cart"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"quantity" : returnquantity }, status=status.HTTP_200_OK)
        if(kwargs['action'] == 'set'):
            product_shop_slug = request.data.get('pslug', None)
            pquantity = request.data.get('quantity', 1)
            if product_shop_slug is None:
                return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
            product_shop = get_object_or_404(
                Product_Shop, slug=product_shop_slug)
            order_product_qs = OrderProduct.objects.filter(
                user=request.user,
                product=product_shop,
                ordered=False
            )
            if order_product_qs.exists():
                order_product = order_product_qs.first()
                order_product.quantity = pquantity
                order_product.save()
            else:
                context = {"user": request.user, "product": product_shop}
                valid_data = {}
                valid_data["ordered"] = False
                valid_data["quantity"] = pquantity
                serializer = self.get_serializer(
                    data=valid_data, context=context)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if not order.products.filter(product__id=order_product.id).exists():
                    order.products.add(order_product)
            else:
                order = Order.objects.create(user=request.user)
                order.products.add(order_product)
            return Response({"quantity": pquantity}, status=HTTP_200_OK)
        if(kwargs['action'] == 'removeall'):
            product_shop_slug = request.data.get('pslug', None)
            if product_shop_slug is None:
                return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
            product_shop = get_object_or_404(
                Product_Shop, slug=product_shop_slug)
            order_product_qs = OrderProduct.objects.filter(
                user=request.user,
                product=product_shop,
                ordered=False
            )
            returnquantity=0

            if order_product_qs.exists():
                order_product = order_product_qs.first()
                order_product.delete()
                order = Order.objects.get(user=request.user, ordered=False)
                if order.products.all().count() <= 0:
                    order.delete()
            else:
                return Response({"message": "Product is not in cart"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"quantity" : returnquantity }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)


class CartViewAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            if order.exists():

                return order[0]
            else:
                return None
        except ObjectDoesNotExist:
            # raise Http404("You do not have an active order")
            return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)


class OrderQuantityUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)
        product_shop = get_object_or_404(Product_Shop, slug=slug)
        if (product_shop.user == request.user):
            order_qs = Order.objects.filter(
                user=request.user,
                ordered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products.filter(product__slug=product_shop.slug).exists():
                    order_product = OrderProduct.objects.filter(
                        product=product_shop,
                        user=request.user,
                        ordered=False
                    )[0]
                    if order_product.quantity > 1:
                        order_product.quantity -= 1
                        order_product.save()
                    else:
                        order.products.remove(order_product)
                    return Response(status=HTTP_200_OK)
                else:
                    return Response({"message": "This item was not in your cart"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "You do not have an active order"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)


class OrderItemDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = OrderProduct.objects.all()


class ShippingAddressViewAPI(generics.GenericAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        data = []
        regular_user = request.user
        addresses = BillingAddress.objects.filter(user=regular_user).distinct()
        serializer = self.get_serializer(addresses, many=True)
        data = serializer.data
        return Response(data)

    def post(self, request, *args, **kwargs):
        regular_user = request.user
        context = {"user": regular_user}
        if (all(x in list(request.data.keys()) for x in ['name', 'contact', 'contact2', 'apartment_address', 'street_address', 'city', 'state', 'area_pincode'])):
            valid_data = {}
            valid_data['name'] = request.data['name']
            valid_data['contact'] = request.data['contact']
            if(request.data['contact2']):
                valid_data['contact2'] = request.data['contact2']
            else:
                valid_data['contact2'] = None
            valid_data['apartment_address'] = request.data['apartment_address']
            valid_data['street_address'] = request.data['street_address']
            valid_data['city'] = request.data['city']
            valid_data['state'] = request.data['state']
            valid_data['area_pincode'] = request.data['area_pincode']
            if(request.data['address_type']):
                valid_data['address_type'] = request.data['address_type']
            else:
                valid_data['address_type'] = 'H'
            if(request.data['default_shipping']):
                valid_data['default_shipping'] = request.data['default_shipping']
            else:
                valid_data['default_shipping'] = False
            if(request.data['default_billing']):
                valid_data['default_billing'] = request.data['default_billing']
            else:
                valid_data['default_billing'] = False
            serializer = self.get_serializer(
                data=valid_data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Fields missing",
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        slug = kwargs['slug']
        if not slug:
            return Response({"message": "Please select an address to delete"}, status=HTTP_400_BAD_REQUEST)
        address = get_object_or_404(BillingAddress, slug=slug)
        if(address.user == request.user):
            address.delete()
            return Response({
                "detail": "Address Removed Successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please select a valid address to delete"}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        slug = kwargs['slug']
        if not slug:
            return Response({"message": "Please select an address to update"}, status=HTTP_400_BAD_REQUEST)
        address = get_object_or_404(BillingAddress, slug=slug)
        if(address.user == request.user):
            serializer = ShippingAddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response({"message": "Please provide valid details"}, status=status.HTTP_400_BAD_REQUEST)

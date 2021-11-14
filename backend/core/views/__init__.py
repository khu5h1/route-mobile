from .order_views import *
from .product_views import *
from .shop_views import *

from rest_framework.response import Response
from rest_framework import status
from core.serializers import ProductSerializer,ShopSerializer
from core.models import Shop, Product
from rest_framework.decorators import api_view
from django.db.models import Q


# TODO : To be optimised

@api_view(('GET',))
def Autocomplete(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        prod_qs = Product.objects.filter(Q(name__contains=query)).distinct()[:10]
        shop_qs = Shop.objects.filter(Q(name__contains=query)).distinct()[:10]
        serializer = ProductSerializer(prod_qs, many=True)
        products = serializer.data
        serializer = ShopSerializer(shop_qs, many=True)
        shops = serializer.data
        result ={"products": [{"name":product["name"],"category":product["category"].values_list("name",flat=True)} for product in products],"shops": [{"name":shop["name"],"locality":shop["locality"],"city":shop["city"], "state":shop["state"]} for shop in shops]}
        return Response(result)
    else:
        return Response({
                "detail": "Invalid Request",
            }, status=status.HTTP_404_NOT_FOUND)

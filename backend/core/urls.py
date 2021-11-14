from django.urls import path
from .views import ProductSearchApi, ProductViewAPI, ProductReviewsAPI, ProductRatingViewAPI, ProductSearchWithCategoryApi
from .views import BusinessShopViewAPI, ShopViewAPI, Autocomplete, ExploreProductsAPI, ShopReviewsAPI, ShopRatingViewAPI, AllShopsViewAPI
from .views import ShippingAddressViewAPI, CartEditAPI, CartViewAPI

app_name = 'core'
urlpatterns = [
    path('product/<slug:slug>/', ProductViewAPI.as_view(),
         name='product'),  # checked correct
    path('search_product/', ProductSearchApi.as_view()),			# checked correct
    path('shops/', BusinessShopViewAPI.as_view()),				# checked correct
    path('shop/<slug:slug>/', ShopViewAPI.as_view()),			# checked correct
    path('productList/', Autocomplete),							# checked correct
    path('explore_shop/<slug:slug>/',
         ExploreProductsAPI.as_view()),  # checked correct
    path('shop-reviews/<slug:slug>/', ShopReviewsAPI.as_view()),		# checked correct
    path('product-reviews/<slug:slug>/',
         ProductReviewsAPI.as_view()),  # checked correct
    path('shop-rating/<slug:slug>/',
         ShopRatingViewAPI.as_view()),		# checked correct
    path('product-rating/<slug:slug>/',
         ProductRatingViewAPI.as_view()),  # checked correct
    # checked correct
    path('address/<slug:slug>/', ShippingAddressViewAPI.as_view()),
    path('address/', ShippingAddressViewAPI.as_view()),
    #     path('address/update/<slug>',
    #          ShippingAddressViewAPI.as_view()),						# checked correct
    # path('orders/', OrderView.as_view()),
    # path('cart/', CartViewAPI.as_view()),
    path('allshops/', AllShopsViewAPI.as_view()),
    path('products/<slug:sslug>/<slug:cslug>/',
         ProductSearchWithCategoryApi.as_view()),
    path('cart/<slug:action>/', CartEditAPI.as_view()),
    path('cart/', CartViewAPI.as_view())
]

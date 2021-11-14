from django.urls import path
from .regular_views import RegisterApi, UserDetails, TokenObtainPairView, TokenVerify, FavouriteShop
from .business_views import BusinessRegisterApi, BusinessVerifyApi, BusinessAccountApi
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('register/', RegisterApi.as_view()),   # checked correct
    path('account_details/', UserDetails.as_view()),    # checked correct
    path('login/', TokenObtainPairView.as_view(),   # checked correct
         name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),  # checked correct
    path('business/register/', BusinessRegisterApi.as_view()),
    path('business/verify/', BusinessVerifyApi.as_view()),
    path('verify/', TokenVerify.as_view()),
    path('favouriteshop/<slug:slug>/', FavouriteShop.as_view()),
    path('favouriteshop/', FavouriteShop.as_view()),
    path('business/account_details/', BusinessAccountApi.as_view()),
    # path('addresses/', AddressViewApi.as_view()),
]

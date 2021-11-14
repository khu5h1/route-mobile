from rest_framework import generics
from rest_framework.response import Response
from .serializer import RegisterSerializer,  AccountSerializer, FavouriteShopSerializer
from rest_framework.permissions import IsAuthenticated
from .models import RegularAccount
from core.models import Shop
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
# from rest_framework_simplejwt.authentication import JWTAuthentication
# TODO remove all print statements from all files

# HELP To authenticate a user
# from django.contrib.auth import authenticate
# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials

# Register API


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        # try:
        valid_data = {}
        if (all(x in list(request.data.keys()) for x in ['mobile', 'email_address', 'fname', 'lname', 'pass'])):
            valid_data['username'] = request.data['mobile']
            valid_data['password'] = request.data['pass']
            valid_data['email'] = request.data['email_address']
            valid_data['first_name'] = request.data['fname']
            valid_data['last_name'] = request.data['lname']
        else:
            return Response({
                "detail": "Fields missing",
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=valid_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = generics.get_object_or_404(
            RegularAccount, username=valid_data['username'])
        valid_data['username'] = user.username
        valid_data['password'] = request.data['pass']
        serializer = serializers.TokenObtainPairSerializer(data=valid_data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenVerify(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        return Response({
            "detail": "Token Verified",
        })

# TODO add proper comments with tests and documentations


class UserDetails(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        # HELP
        # token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        user_details = request.user
        serializer = AccountSerializer(user_details)
        return Response(  # { HELP
            # "user": str(JWTAuthentication().get_user(validated_token=JWTAuthentication().get_validated_token(token))),
            # "user": request.GET.get("username", " ").split(','),
            # 'user': request.method,}
            serializer.data
        )

    # TODO to be optimized as it is saving the changes twice in the backend
    def post(self, request, *args, **kwargs):

        user_details = request.user
        request_fields = request.data.keys()
        if(request.GET['query'] == 'change_details'):
            valid_data = {'user': {}, }
            if ('mobile' in request_fields):
                if int(request.data['mobile']) <= 9999999999 and int(request.data['mobile']) > 1000000000:
                    user_details.username = int(request.data['mobile'])
                    valid_data['username'] = int(request.data['mobile'])
                else:
                    return Response({"message": "Invalid mobile"}, status=status.HTTP_400_BAD_REQUEST)
            if ('email_address' in request_fields):
                user_details.email = request.data['email_address']
                valid_data['email'] = request.data['email_address']

            if('fname' in request_fields):
                user_details.first_name = request.data['fname']
                valid_data['first_name'] = request.data['fname']

            if('lname' in request_fields):
                user_details.last_name = request.data['lname']
                valid_data['last_name'] = request.data['lname']

            if('dob' in request_fields):
                user_details.dob = request.data['dob']
                valid_data['dob'] = request.data['dob']

            if('gender' in request_fields):
                user_details.gender = request.data['gender']
                valid_data['gender'] = request.data['gender']
            user_details.save()
            serializer = AccountSerializer(user_details, data=valid_data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        elif (request.GET['query'] == 'change_pass'):
            if ('new_pass' in request_fields and 'old_pass' in request_fields):
                if(request.user.check_password(request.data['old_pass'])):
                    request.user.set_password(request.data['new_pass'])
                    request.user.save()
                    return Response({
                        "detail": "Password Update Successful",
                    })
                else:
                    return Response({
                        "detail": "Please enter a valid old password",
                    }, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({
                    "detail": "Please provide valid fields",
                }, status=status.HTTP_400_BAD_REQUEST)


# TODO: make TokenObtainPairView functional with email or phone instead of userid/username

class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        valid_data = {}
        userid = request.data['userid']

        if('@' in userid):
            user = generics.get_object_or_404(
                RegularAccount, email=userid)
        else:
            user = generics.get_object_or_404(RegularAccount, username=userid)
        valid_data['username'] = user.username
        valid_data['password'] = request.data['pass']
        serializer = self.get_serializer(data=valid_data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class FavouriteShop(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user_details = request.user
        serializer = FavouriteShopSerializer(user_details)
        return Response(  # { HELP
            # "user": str(JWTAuthentication().get_user(validated_token=JWTAuthentication().get_validated_token(token))),
            # "user": request.GET.get("username", " ").split(','),
            # 'user': request.method,}
            serializer.data
        )

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        try:
            request.user.favourite_shops.add(Shop.objects.get(slug=slug))
            return Response({
                "detail": "Shop added to favourites"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "detail": "Invalid Request"
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        try:
            request.user.favourite_shops.remove(
                Shop.objects.get(slug=slug))
            return Response({
                "detail": "Shop removed to favourites"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "detail": "Invalid Request"
            }, status=status.HTTP_400_BAD_REQUEST)


# AddressViewAPI moved to OrderViews

# class AddressViewApi(generics.GenericAPIView):
#     pagination_class = CustomPagination
#     serializer_class = BillingAddressSerializer
#     permission_classes = [IsAuthenticated, ]

#     # returns list of addresses of the given user
#     def get(self, request, *args, **kwargs):
#         data = []
#         results = BillingAddress.objects.filter(user = request.user).distinct()
#         page = self.paginate_queryset(results)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             result = self.get_paginated_response(serializer.data)
#             data = result.data  # pagination data
#         else:
#             serializer = self.get_serializer(results, many=True)
#             data = serializer.data
#         return Response(data)

#     def post(self, request, *args, **kwargs):
#         if(request.GET['query'] == 'add'):
#             context = {"user": request.user}
#             serializer = self.get_serializer(data=request.data, context=context)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response({
#                 "detail": "Address Added Successfully",
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "detail" : "Please provide a query"
#             }, status=status.HTTP_400_BAD_REQUEST)

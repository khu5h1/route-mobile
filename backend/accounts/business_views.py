from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import BusinessRegisterSerializer, BusinessAccountSerializer
from .models import RegularAccount, BusinessAccount
from rest_framework_simplejwt import serializers
from rest_framework import generics
from rest_framework import status


class BusinessRegisterApi(generics.GenericAPIView):
    serializer_class = BusinessRegisterSerializer
    permission_classes = [IsAuthenticated, ]

    # TODO add more fields for SignUp of businessman

    def post(self, request, *args, **kwargs):
        valid_data = {}
        if (all(x in list(request.data.keys()) for x in ['pan_no'])):
            valid_data['pan_number'] = request.data['pan_no']
        else:
            return Response({
                "detail": "Fields Missing"
            }, status=status.HTTP_400_BAD_REQUEST)
        # TODO to be chnaged as per new regular account implementation
        user = request.user
        if (user.isbusiness):
            return Response({
                "detail": "Already a Business Account"
            }, status=status.HTTP_400_BAD_REQUEST)
        context = {"user": request.user}
        serializer = self.get_serializer(data=valid_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.isbusiness = True
        user.save()
        return Response({
            "detail": "Business Account Registered Successfully"
        }, status=status.HTTP_200_OK)


class BusinessVerifyApi(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        if (request.user.isbusiness):
            return Response({
                "detail": "It is a Business Account"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "It is not a Business Account"
            }, status=status.HTTP_401_UNAUTHORIZED)


class BusinessAccountApi(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user_details = BusinessAccount.objects.get(
            user=request.user)
        serializer = BusinessAccountSerializer(user_details)
        return Response(serializer.data)

# TODO to be optimized as it is saving the changes twice in the backend
    def post(self, request, *args, **kwargs):
        user_details = BusinessAccount.objects.get(user=request.user)
        request_fields = request.data.keys()
        valid_data = {}
        if ('pan' in request_fields):
            user_details.pan_number = request.data['pan']
            valid_data['pan_number'] = request.data['pan']
        user_details.save()
        serializer = BusinessAccountSerializer(user_details, data=valid_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

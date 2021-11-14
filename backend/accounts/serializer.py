from rest_framework import serializers
from .models import RegularAccount, BusinessAccount, BillingAddress
from .models import RegularAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django.conf import settings

# TODO : to add validations for each and every field we receive


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegularAccount
        fields = '__all__'

    def create(self, validated_data):
        user = RegularAccount.objects.create_user(validated_data['username'], password=validated_data['password'],
                                                  first_name=validated_data['first_name'],
                                                  last_name=validated_data['last_name'],
                                                  email=validated_data['email'])
        return user

    def is_valid(self, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = {"detail":
                                "A user with that email or contact already exists or The data you entered is not valid", }
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)
# END serializers for Registeration of user


# TODO change the field_names as we don't want user to see the original fieldname
class BusinessRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessAccount
        fields = ('pan_number', )

    def create(self, validated_data):
        business_account = BusinessAccount.objects.create(
            user=self.context.get("user"), pan_number=validated_data['pan_number'])
        return business_account


# START serializer for Regular Account with all fields
class AccountSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField('get_username')
    email_address = serializers.SerializerMethodField(
        'get_email')
    fname = serializers.SerializerMethodField('get_first_name')
    lname = serializers.SerializerMethodField('get_last_name')

    class Meta:
        model = RegularAccount
        # fields = '__all__'
        fields = ('userid', 'email_address',
                  'fname', 'lname', 'dob', 'gender')

    def get_username(self, obj):
        return obj.username

    def get_email(self, obj):
        return obj.email

    def get_first_name(self, obj):
        return obj.first_name

    def get_last_name(self, obj):
        return obj.last_name


class BusinessAccountSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField('get_username')
    email_address = serializers.SerializerMethodField(
        'get_email')
    fname = serializers.SerializerMethodField('get_first_name')
    lname = serializers.SerializerMethodField('get_last_name')
    pan = serializers.SerializerMethodField('get_pan_number')

    class Meta:
        model = BusinessAccount
        # fields = '__all__'
        fields = ('userid', 'email_address',
                  'pan', 'fname', 'lname',)

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_pan_number(self, obj):
        return obj.pan_number

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class BillingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingAddress
        fields = ('name', 'contact', 'contact2', 'apartment_address',
                          'street_address', 'area_pincode', 'state')

    def create(self, validated_data):
        address = BillingAddress.objects.create(
            user=self.context.get('user'), name=validated_data['name'], contact=validated_data['contact'], contact2=validated_data['contact2'],
            apartment_address=validated_data['apartment_address'], street_address=validated_data['street_address'],
            area_pincode=validated_data['area_pincode'], state=validated_data['state'])
        return address


class FavouriteShopSerializer(serializers.ModelSerializer):
    favshops = serializers.SerializerMethodField()

    class Meta:
        model = RegularAccount
        # fields = '__all__'
        fields = ('favshops', )

    def get_favshops(self, obj):
        return obj.get_favourite_shops_slug()


# END serializer for Regular Account with all fields


# HELP pass custom claim params with token
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['name'] = user.name
#         # ...

#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

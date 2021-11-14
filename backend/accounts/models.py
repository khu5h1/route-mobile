from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from backend.utils import address_slug_generator
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


ADDRESS_CHOICES = (
    ('H', 'Home'),
    ('W', 'Work'),
    ('O', 'Other')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class RegularAccount(AbstractUser):
    username = models.IntegerField(validators=[MaxValueValidator(
        9999999999), MinValueValidator(1000000000)], unique=True)
    email = models.EmailField(
        _('email address'), unique=True, null=True, default=None, blank=True)
    isbusiness = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    favourite_shops = models.ManyToManyField(
        "core.shop",  blank=True)
    dob = models.DateField(
        auto_now_add=False, default=None, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=None, blank=True, null=True)

    def save(self, **kwargs):
        self.email = self.email or None
        super().save(**kwargs)

    def __str__(self):
        return str(self.username)

    def get_address(self):
        return self.address.all()

    def get_business(self):
        return self.business

    def get_product_reviews(self):
        return self.product_reviews.all()

    def get_shop_reviews(self):
        return self.shop_reviews.all()

    def get_favourite_shops_slug(self):
        return self.favourite_shops.values_list("slug", flat=True)


class BusinessAccount(models.Model):
    # Add related fields for BusinessAccount
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business')
    pan_number = models.CharField(max_length=10, validators=[
        RegexValidator(r"([A-Z]{5}[0-9]{4}[A-Z]{1})"), ], unique=True, null=False, blank=False)

    def __str__(self):
        return str(self.user.username)

    def get_shops(self):
        return self.shops.all()


class BillingAddress(models.Model):
    # TODO set the first added address as default billing/shipping initially
    class Meta:
        verbose_name = 'BillingAddress'
        verbose_name_plural = 'BillingAddresses'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='address')
    name = models.CharField(max_length=50, null=False, blank=False)
    contact = models.IntegerField(
        validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], null=False, blank=False)
    contact2 = models.IntegerField(validators=[MaxValueValidator(
        9999999999), MinValueValidator(1000000000)], null=True, blank=True)
    apartment_address = models.CharField(
        max_length=100, null=False, blank=False)
    street_address = models.CharField(max_length=100, null=False, blank=False)
    area_pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r"([1-9]{1}[0-9]{5})"), ], null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    address_type = models.CharField(
        max_length=1, choices=ADDRESS_CHOICES, default="W", null=False, blank=False)
    default_shipping = models.BooleanField(
        default=False, null=False, blank=False)
    default_billing = models.BooleanField(
        default=False, null=False, blank=False)
    slug = models.SlugField(max_length=150, blank=True, null=True)

    # country = CountryField(multiple=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_address_check"),

        ]

    def __str__(self):
        return self.name

    def get_user(self):
        return self.user.username


# class Coupon(models.Model):
#     code = models.CharField(max_length=15)
#     amount = models.FloatField()

#     def __str__(self):
#         return self.code


# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     accepted = models.BooleanField(default=False)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.pk}"


# def userprofile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         userprofile = UserProfile.objects.create(user=instance)


# post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

# """Use this to sligfy the fields"""
# def pre_save_blog_post_receiever(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		instance.slug = slugify(instance.author.username + "-" + instance.title)

# pre_save.connect(pre_save_blog_post_receiever, sender=BlogPost)


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = address_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=BillingAddress)

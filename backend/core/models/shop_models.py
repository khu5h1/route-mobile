from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.fields import DateTimeField
from accounts.models import BusinessAccount, RegularAccount
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save, post_save
from backend.utils import unique_slug_generator
from django.conf import settings
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.slug:
            filename = '{}.{}'.format(instance.slug, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

# TODO : delete image explicitly if shopkeeper changes the display image


class Shop(models.Model):
    business = models.ForeignKey(
        BusinessAccount, models.CASCADE, related_name='shops')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    gstin_number = models.CharField(max_length=15, validators=[RegexValidator(
        r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}")], unique=True, null=False, blank=False)
    longitude = models.DecimalField(
        max_digits=19, decimal_places=10, null=False, blank=False)
    latitude = models.DecimalField(
        max_digits=19, decimal_places=10, null=False, blank=False)
    contact = models.IntegerField(
        validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], unique=True, null=False, blank=False)
    contact2 = models.IntegerField(validators=[MaxValueValidator(
        9999999999), MinValueValidator(1000000000)], null=True, blank=True)
    address = models.CharField(
        max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    area_pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r"([1-9]{1}[0-9]{5})"), ], null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    products_categories = models.ManyToManyField(
        'Category', blank=False)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    total_reviews = models.IntegerField(default=0)
    open_time = models.TimeField(null=False, blank=False)
    close_time = models.TimeField(null=False, blank=False)
    # This will store closed days in the form: Saturday,Sunday
    # TODO while creating the api for this please keep in mind to check that closed days are from MTWTFS
    closed_days = models.TextField(default=None, blank=True, null=True)
    image = models.ImageField(
        upload_to=UploadToPathAndRename('shops'), max_length=200)

    # If the above approach didn't worked we will use the below-mentioned approach
    # open_hour = models.IntegerField(validators=[MaxValueValidator(24), MinValueValidator(0)])
    # open_minute = models.IntegerField(validators=[MaxValueValidator(59), MinValueValidator(0)])
    # close_hour = models.IntegerField(validators=[MaxValueValidator(24), MinValueValidator(0)])
    # close_minute = models.IntegerField(validators=[MaxValueValidator(59), MinValueValidator(0)])
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["longitude", "latitude"], name="unique_location_check"),
            models.UniqueConstraint(
                fields=["business", "gstin_number"], name="unique_gstin_check"),
            models.UniqueConstraint(
                fields=["business", "name"], name="unique_business_name_check"),
            models.UniqueConstraint(
                fields=["address", "street", "area_pincode", "city", "state"], name="unique_address_check")
        ]

    def __str__(self):
        return str(self.name)

    def get_products(self):
        return self.products.all()

    def get_owner(self):
        return str(self.business.regular_account.username)

    def get_categories_name(self):
        return self.products_categories.values_list("name", flat=True)

    def get_reviews(self):
        return self.reviews.all()


class ShopReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='shop_reviews')
    shop = models.ForeignKey(Shop, models.CASCADE, related_name='reviews')
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField()

    class Meta:
        unique_together = ("user", "shop")


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def review_post_save(sender, instance, *args, **kwargs):
    shop_total_reviews = instance.shop.total_reviews
    new_rating = (instance.shop.rating*shop_total_reviews +
                  instance.rating)/(shop_total_reviews+1)
    shop = Shop.objects.get(pk=instance.shop.id)
    shop.total_reviews = shop_total_reviews + 1
    shop.rating = new_rating
    shop.save(update_fields=['total_reviews', 'rating'])


pre_save.connect(pre_save_receiver, sender=Shop)
post_save.connect(review_post_save, sender=ShopReview)

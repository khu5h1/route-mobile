from django.db import models
from django.conf import settings
import jsonfield
from .shop_models import Shop
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from backend.utils import unique_slug_generator, product_shop_slug_generator
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from accounts.models import RegularAccount
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.product.slug:
            filename = '{}/{}.{}'.format(instance.product.slug,
                                         uuid4().hex, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    # will store in such a way:- proerty1,property2,property3 etc..
    other_details = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_products(self):
        return self.products.all()


class ProductImage(models.Model):
    product = models.OneToOneField(
        "Product", primary_key=True, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        upload_to=UploadToPathAndRename('products'), max_length=200)

    def __str__(self):
        return self.product.name

# TODO change slug field to primary in all tables or find something better for indexing


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    slug = models.SlugField(max_length=150, blank=True, null=True)
    mrp = models.DecimalField(
        decimal_places=2, max_digits=19, null=False, blank=False)
    hsn_code = models.IntegerField(null=False, blank=False)
    # discounted_price = models.DecimalField(decimal_places=2, max_digits=19)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    total_reviews = models.IntegerField(default=0)
    weight = models.DecimalField(decimal_places=4, max_digits=19)
    # TODO add checks to make seller add products only in the category he sales.
    category = models.ManyToManyField(
        Category, related_name="category",  blank=False)
    seller = models.ManyToManyField(
        Shop, related_name="products", through="Product_Shop",  blank=False)
    # HELP json field reference
    # https://github.com/adamchainz/django-jsonfield/blob/master/jsonfield/tests/test_fields.py
    other_details = models.TextField()

    def __str__(self):
        return self.name

    def get_categories(self):
        return self.category.all()

    def get_categories_name(self):
        return self.category.values_list("name", flat=True)

    def get_sellers(self):
        return self.seller.all()

    def get_reviews(self):
        return self.reviews.all()

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})


class Product_Shop(models.Model):
    product = models.ForeignKey(Product, models.CASCADE)
    seller = models.ForeignKey(Shop, models.CASCADE)
    variant = models.ForeignKey(
        "Product_Variant", on_delete=models.CASCADE, default=None, blank=True, null=True)
    seller_price = models.DecimalField(decimal_places=2, max_digits=19)
    sku = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=300, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seller", "sku"], name="unique_seller_sku_check"),
        ]


class Product_Variant(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mrp = models.DecimalField(decimal_places=2, max_digits=19)
    # TODO separate image field for each variant
    other_details = models.TextField()

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='product_reviews')
    product = models.ForeignKey(
        Product, models.CASCADE, related_name='reviews')
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField()


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def product_shop_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = product_shop_slug_generator(instance)


def review_post_save(sender, instance, *args, **kwargs):
    product_total_reviews = instance.product.total_reviews
    new_rating = (instance.product.rating*product_total_reviews +
                  instance.rating)/(product_total_reviews+1)
    product = Product.objects.get(pk=instance.product.id)
    product.total_reviews = product_total_reviews + 1
    product.rating = new_rating
    product.save(update_fields=['total_reviews', 'rating'])


pre_save.connect(pre_save_receiver, sender=Product)
pre_save.connect(product_shop_pre_save_receiver, sender=Product_Shop)
post_save.connect(review_post_save, sender=ProductReview)


# TODO: Create a separate Variation model for products like pack of 2 or 4 if needed in future

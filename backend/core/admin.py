from django.contrib import admin
from .models import Shop, Product, Category, Product_Shop, ShopReview, ProductReview, Order, OrderProduct, ProductImage, Product_Variant
# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Product_Shop)
admin.site.register(ShopReview)
admin.site.register(ProductReview)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ProductImage)
admin.site.register(Product_Variant)

from django.conf import settings
from django.db import models
import jsonfield
from .product_models import Product_Shop, Product_Variant
from accounts.models import RegularAccount, BillingAddress

# TODO : To be optimised

# TODO add order reference number and it's generator


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product_Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sold_price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.product.name}"

    def get_total_product_mrp_price(self):
        return self.quantity * self.product.product.price

    def get_total_seller_product_price(self):
        if self.sold_price:
            return self.quantity * self.sold_price
        else:
            return self.quantity * self.product.seller_price

    def get_seller_name(self):
        return self.product.seller.name

    def get_amount_saved(self):
        benefit = self.get_total_product_mrp_price() - self.get_total_seller_product_price()
        if(benefit < 0):
            benefit = 0
        return benefit

    def get_final_price(self):
        if self.product.seller_price:  # it is a required field currently, so maybe make it optional in the model or remove from here
            return self.get_total_seller_product_price()
        return self.get_total_product_mrp_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    # if not ordered, then leave blank
    ordered_date = models.DateTimeField(blank=True, default=None, null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_billing_address')
    shipping_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_shipping_address')

    # coupon = models.ForeignKey(
    # 'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    # payment method to be added later
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total

    def get_order_products(self):
        return self.orderproduct.all()
    
    def get_total_products_quantity(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.quantity
        return total

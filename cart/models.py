from django.db import models
from product.models import SubProductAttribute,ProductQuantity
from accounts.models import UserAddress
# Create your models here.

from django.conf import settings
User=settings.AUTH_USER_MODEL


class Cart(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user_cart_is_auth')
    product = models.ForeignKey(SubProductAttribute,on_delete=models.CASCADE,related_name='user_cart_product')
    product_quantity = models.ForeignKey(ProductQuantity,on_delete=models.CASCADE,related_name='user_cart_product_quantity')
    session_id = models.CharField(max_length=255,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(blank=True,null=True)
    product_qty = models.IntegerField(default=1)
    unit_price = models.DecimalField(decimal_places=2,max_digits=8)
    totel_unit_price = models.DecimalField(decimal_places=2,max_digits=8)
    product_price = models.DecimalField(decimal_places=2,max_digits=8)
    totel_qty_price=  models.DecimalField(decimal_places=2,max_digits=15)
    is_active =     models.BooleanField(default=True)

    def __str__(self):
        return self.product.product.product_name

    def save(self, *args, **kwargs):
        self.totel_unit_price = self.unit_price*self.product_qty
        return super().save(*args, **kwargs)
    

class Coupon(models.Model):
    coupon = models.CharField(max_length=255,blank=True,null=True)
    expiry_date = models.DateTimeField(blank=True,null=True)
    persentage_off = models.FloatField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    gtr_price = models.DecimalField(decimal_places=2,max_digits=8)
    minus_pers = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_id      =   models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='Coupon_created_id',blank=True,null=True)
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_date   =   models.DateTimeField(auto_now=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='Coupon_modified_id',blank=True,null=True)
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created',blank=True,null=True)  
    
    def __str__(self):
        return self.coupon
              
    def save(self, *args, **kwargs):
        pers = self.persentage_off / 100
        minus_pers = 1 - pers
        self.minus_pers = minus_pers
        return super().save(*args, **kwargs)


class RedeamCoupen(models.Model):
    coupon          =   models.ForeignKey(Coupon,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='user_redeam_coupen_is_auth')
    created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user_redeam_coupen_is_auth')
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    is_active       =   models.BooleanField(default=True)
    
    
class Order(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_is_auth')
    products = models.ManyToManyField(Cart,related_name='products')
    delivery_address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL,blank=True,null=True,related_name='user_order_address_is_auth')
    order_confirmation_email = models.EmailField(blank=True,null=True)
    orders_id = models.CharField(max_length=500,unique=True,blank=True,null=True)
    totel_quantity =  models.IntegerField(default=1)
    totel_unit_price = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    totel_offer_price = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    offer_savings_price = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    coupon_text = models.CharField(max_length=255,blank=True,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='user_order_coupen_is_auth')
    coupon_price =  models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    coupon_savings_price = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    order_date = models.DateTimeField(blank=True,null=True)
    order_status = models.CharField(max_length=255,blank=True,null=True)
    totel_payment_price= models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    is_active = models.BooleanField(default=False)
    ip  =   models.GenericIPAddressField(null=True, blank=True,)
    coupen_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)


class CancelReasons(models.Model):
    reasons=models.CharField(max_length=255,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    is_active =     models.BooleanField(default=False)
    created_id      =   models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True, blank=True,related_name='cancel_created_id')
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True, blank=True,related_name='cancel_modified_id')
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created')  
    def __str__(self) :
        return self.reasons



class OrderStatus(models.Model):
    order =  models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_status')
    order_confirmed = models.BooleanField(default=False)
    order_confirmed_date = models.DateTimeField(blank=True,null=True)
    Shipped = models.BooleanField(default=False)
    Shipped_date = models.DateTimeField(blank=True,null=True)
    out_for_delivery = models.BooleanField(default=False)
    out_for_delivery_date = models.DateTimeField(blank=True,null=True)
    delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(blank=True,null=True)
    delivery_execept_date =  models.DateField(blank=True,null=True)
    Cancelled = models.BooleanField(default=False)
    cancelReasons = models.ForeignKey(CancelReasons,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='user_order_CancelReasons_status')
    cancel_reason_descrition=models.TextField(blank=True,null=True)
    cancelled_date = models.DateTimeField(blank=True,null=True)
    current_status = models.IntegerField(blank=True,null=True)   
    is_active = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.order_confirmed == True:
            self.current_status=1
        if self.Shipped == True:
            self.current_status=2    
        if self.out_for_delivery == True:
            self.current_status=3
        if self.delivered == True:
            self.current_status=4 
        if self.Cancelled == True:
            self.current_status=5 
        return super().save(*args, **kwargs)

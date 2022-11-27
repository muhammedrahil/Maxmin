from re import X
from django.db import models
from cart.models import *
from django.conf import settings
User=settings.AUTH_USER_MODEL
# Create your models here.

class CashOnDeliveryTextGenarator(models.Model):
    text = models.CharField(max_length=255,blank=True,null=True)
    is_active =     models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Payment(models.Model):
    order =  models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_payment_status')
    user =  models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_payment_user')
    order_status =  models.ForeignKey(OrderStatus,on_delete=models.CASCADE,blank=True,null=True,related_name='order_payment')
    payment_method = models.CharField(max_length=255,blank=True,null=True)
    payment_order_id = models.CharField(max_length=255,blank=True,null=True)
    payment_id = models.CharField(max_length=255,blank=True,null=True)
    signature = models.CharField(max_length=255,blank=True,null=True)
    payer_id = models.CharField(max_length=255,blank=True,null=True)
    payment_price = models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    payment_date = models.DateTimeField(blank=True,null=True)
    ip  =   models.GenericIPAddressField(null=True, blank=True,)
    payment_status = models.CharField(max_length=255,blank=True,null=True)
    payment_complete_status=models.BooleanField(default=False)
    is_active =     models.BooleanField(default=False)


class RefundPayment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user_refund_payment_user')
    order =  models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_refund_payment_status')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True,related_name='user_order_refund_payment_instence')
    order_status =  models.ForeignKey(OrderStatus,on_delete=models.CASCADE,blank=True,null=True,related_name='refund_payment')
    refund_status=models.BooleanField(default=False)
    execept_refund_date= models.DateField(blank=True,null=True)
    refund_date = models.DateTimeField(blank=True,null=True)
    refund_compleate_status=models.BooleanField(default=False)
    is_active =     models.BooleanField(default=True)
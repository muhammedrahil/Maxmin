from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
        list_display = ['user','product','product_quantity','session_id','created_date','modify_date','deleted_date','product_qty'
                        ,'unit_price','totel_unit_price','product_price','totel_qty_price','is_active']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
        list_display = ['coupon','created_date','expiry_date','persentage_off','is_active']

@admin.register(RedeamCoupen)
class RedeamCoupenAdmin(admin.ModelAdmin):
        list_display = ['coupon','created_date','created_id','created_ip','is_active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
        list_display = ['id','user','delivery_address','order_confirmation_email','orders_id','totel_quantity','totel_unit_price','totel_offer_price','offer_savings_price','coupon_text'
                        ,'coupon','coupon_price','coupon_savings_price','order_date','order_status','ip','totel_payment_price','coupen_active','created_date','modify_date','is_active']

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
        list_display = ['id','order','order_confirmed','order_confirmed_date','Shipped','Shipped_date','out_for_delivery','out_for_delivery_date','delivered'
                        ,'delivered_date','delivery_execept_date','Cancelled','cancelReasons','cancelled_date','current_status','is_active']


@admin.register(CancelReasons)
class CancelReasonsAdmin(admin.ModelAdmin):
        list_display = ['reasons','created_date','modify_date','is_active']
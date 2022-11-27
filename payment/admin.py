from django.contrib import admin
from .models import Payment,CashOnDeliveryTextGenarator,RefundPayment
# Register your models here.

@admin.register(CashOnDeliveryTextGenarator)
class CashOnDeliveryTextGenaratorAdmin(admin.ModelAdmin):
        list_display = ['text','is_active']
        
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
        list_display = ['order','user','order_status','payment_method','payment_order_id','payment_id','payer_id','ip','signature','payment_price','payment_date','payment_status','is_active','payment_complete_status']
        
        
@admin.register(RefundPayment)
class RefundPaymentAdmin(admin.ModelAdmin):
        list_display = ['user','order','order_status','refund_status','execept_refund_date','refund_date','refund_compleate_status','is_active']
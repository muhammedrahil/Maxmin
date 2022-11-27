from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Product)
class ProductCategoryAdmin(admin.ModelAdmin):
        list_display = [
       'pk', 'category','product_name','slug','unit_price','main_image','rating','is_active','product_totel_stoke','created_date','created_id','created_ip','modified_date','modified_id','modified_ip','record_status'
        ]
        prepopulated_fields = {'slug': ('product_name',)}
        # list_filter = ['is_active','record_status','modified_date']
        
@admin.register(SubProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
        list_display = ['pk','product','sub_product_totel_stoke','sku','rating','product_color','offerprice','offer_expiry_date','is_active','created_date','modified_date']


@admin.register(ProductQuantity)
class ProductQuantityAdmin(admin.ModelAdmin):
        list_display = ['product','product_size','quantity','is_active','created_date','modified_date']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
        list_display = ['product','rating','subject','product_image','is_active','created_date','created_id',
                'created_ip','modified_date','modified_id','modified_ip','record_status']
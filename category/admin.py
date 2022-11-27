from django.contrib import admin
from .models import *
# Register your models here.
from mptt.admin import DraggableMPTTAdmin
from product.models import Product


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "category"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('category',)}
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
    
admin.site.register(Category,CategoryAdmin)



@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
        list_display = [
        'id','category','Size','slug','discription','is_active',
        'created_date','created_id','created_ip','modified_date','modified_id','modified_ip','record_status'
        ]
        prepopulated_fields = {'slug': ('Size',)}
        list_filter = ['is_active','record_status','modified_date']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
        list_display = [
        'title','slug','brand_images','discription','is_active',
        'created_date','created_id','created_ip','modified_date','modified_id','modified_ip','record_status'
        ]
        list_filter = ['is_active','record_status','modified_date']
        prepopulated_fields = {'slug': ('title',)}
        
        
        
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
        list_display = [
        'title','color_code','slug','discription','is_active',
        'created_date','created_id','created_ip','modified_date','modified_id','modified_ip','record_status'
        ]
        list_filter = ['is_active','record_status','modified_date']
        prepopulated_fields = {'slug': ('title','color_code',)}
        
@admin.register(GenderCategory)
class GenderCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'gender','is_active',
        'created_date','created_id','created_ip','modified_date','modified_id','modified_ip','record_status'
        ]
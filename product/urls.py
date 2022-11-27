from django.urls import path
from . import admin_product as a
from . import user_product_section as u
from . import sub_product_admin as s
from . import admin_quantity_size as ad
from . import sales as sa
from . import review as rw


app_name = 'product'


urlpatterns = [
    
    path('sub-product/<str:pk>',s.sub_product,name='sub_product'),
    path('add-sub-product/<int:pk>',s.add_sub_product,name='add_sub_products'),
    path('sub-product-active',s.sub_product_active,name='sub_product_active'),
    path('sub-delete-product',s.sub_delete_product,name='sub_delete_product'),
    path('edit-sub-product/<str:pk>',s.edit_sub_product,name='edit_sub_product'),
    path('edit_sub_product_form/<int:sub_pk>',s.edit_sub_product_form,name='edit_sub_product_form'),
    
    path('add-sub-product-qauntity/<str:pk>&<str:sub_pk>',ad.add_sub_product_qauntity,name='add_sub_product_qauntity'),
    path('add-size-quantity',ad.add_size_quantity,name='add_size_quantity'),
    path('edit-size-quantity',ad.edit_size_quantity,name='edit_size_quantity'),
    path('delete-size-qty',ad.delete_size_qty,name='delete_size_qty'),
    
    path('??/<int:pk>/<slug:product_name>/<int:genter>',u.all_categories,name="allcategories"),
    path('?/filter-data',u.filter_data,name='filter_data'),
    path('<slug:product_slug>/<int:single_Productdeatail_pk>',u.single_Productdeatail,name="single_Productdeatail"),
    path('filterprice',u.filterprice,name='filterprice'),
    
    
    path('All-product',a.admin_product,name='admin_product'),
    path('add-product',a.add_product,name='add_product'),
    path('product-active',a.product_active,name='product_active'),
    path('edit-product',a.edit_product,name='edit_product'),
    path('delete-product',a.delete_product,name='delete_product'),
    path('change-image-product',a.change_image_product,name='change_image_product'),
    
    path('sales-report',sa.sales_report,name='sales_report'),
    path('date-filter',sa.date_filter,name='date_filter'),
    
    path('product-review??#&*<int:pk>??#&*',rw.product_review,name='product_review'),
    
]
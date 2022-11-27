from django.urls import path
from . import admin_category as ac
from . import admin_size as az
from . import color_admin as ca
from . import brand_admin as ba
from . import gender_category as gc



app_name = 'category'
urlpatterns = [
    
    path('category',ac.Category.as_view(),name='category'),
    path('add-category',ac.add_category,name='add_category'),
    path('delete-category',ac.delete_category,name='delete_category'),
    path('category-active',ac.category_active,name='category_active'),
    path('edit-category',ac.edit_category,name='edit_category'),
    
    path('size',az.Size.as_view(),name='size'),
    path('add-size',az.add_size,name='add_size'),
    path('edit-size',az.edit_size,name='edit_size'),
    path('delete-size',az.delete_size,name='delete_size'),
    path('size-is-active',az.size_is_active,name='size_is_active'),
    
    path('color',ca.Color.as_view(),name='color'),
    path('add-color',ca.add_color,name='add_color'),
    path('edit-color',ca.edit_color,name='edit_color'),
    path('delete-color',ca.delete_color,name='delete_color'),
    path('color-is-active',ca.color_is_active,name='color_is_active'),
    
    path('brand',ba.Brand.as_view(),name='brand'),
    path('add-brand',ba.add_brand,name='add_brand'),
    path('edit-brand/<int:pk>',ba.edit_brand,name='edit_brand'),
    path('delete-brand',ba.delete_brand,name='delete_brand'),
    path('delete-brand-category',ba.delete_brand_category,name='delete_brand_category'),
    path('brand-is-active',ba.brand_is_active,name='brand_is_active'),
    
    path('gender_category',gc.gender_category,name='gender_category'),
    path('add_gender_category',gc.add_gender_category,name='add_gender_category'),
    path('gender_category_is_active',gc.gender_category_is_active,name='gender_category_is_active'),
    path('gender_category_delete',gc.gender_category_delete,name='gender_category_delete'),
    path('edit_gender_category',gc.edit_gender_category,name='edit_gender_category'),
    

]
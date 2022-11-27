from django.urls import path
from . import views as v
from . import dashboard as d
from . import banner as b

app_name = 'landing'
urlpatterns = [
    path('',v.landing_page,name='landing_page'),
    path('dashboard',d.dashboard,name="dashboard"),
    
    path('banner',b.banner,name="banner"),
    path('add-banner/<int:pk>',b.add_banner,name="add_banner"),
    path('change-banner',b.change_banner,name="change_banner"),
    path('active-banner',b.active_banner,name="active_banner"),
    path('edit-banner/<int:pk>',b.edit_banner,name="edit_banner"),
    path('banner-delete-product',b.banner_delete_product,name="banner_delete_product"),
    
    
    
    
    
    
]
from django.urls import path
from . import views as v
from . import checkout as c
from . import order as o
from . import admin_order as ao
from . import coupen as co
from . import user_coupen as uc




app_name = 'cart'
urlpatterns = [
    
    path('',v.add_to_cart,name='add_to_cart'),
    path('quantity',v.quantity,name='quantity'),
    path('view-cart',v.cart,name='cart'),
    path('price-change',v.price_change,name='price_change'),
    path('size-change',v.size_change,name='size_change'),
    path('delete-cart-items',v.deleted_cart_items,name='deleted_cart_items'),
    
    path('checkout',c.checkout,name='checkout'),
    path('delivery-address',c.delivery_address,name='delivery_address'),
    path('delete-checkout-items',c.delete_checkout_items,name='delete_checkout_items'),
    
    
    path('continue-order',o.continue_order,name='continue_order'),
    path('coupon',o.coupon,name='coupon'),

    path('order',ao.order,name='order'),
    path('order&<str:pay_id>&<str:status_id>&<str:order_id>',ao.order_deatails,name='order_deatails'),
    path('update-status/<int:pk>',ao.update_status,name='update_status'),
    
    path('coupen_list',co.coupen_list,name='coupen_list'),
    path('add-coupen',co.add_coupen,name='add_coupen'),
    path('coupen-is-active',co.coupen_is_active,name='coupen_is_active'),
    path('coupen-delete',co.coupen_delete,name='coupen_delete'),
    path('edit-coupen',co.edit_coupen,name='edit_coupen'),

    path('user-coupen',uc.user_coupen,name='user_coupen'),
    
]
from django.urls import path
from . import orders_placed as v
from . import razorpay as r
from . import paypal as p
from . import invoice as i
from . import refund as re
from . import cancel_reasons as cr
from . import cash_on_delivery_text as ct

app_name = 'payment'

urlpatterns = [
    path('text-genarator',v.cash_on_delivery_code_genarator,name='cash_on_delivery_code_genarator'),
    path('cash-on-delivery-order-confrim/<str:product_order_session_id>/',v.cash_on_delivery_order_confrim,name='cash_on_delivery_order_confrim'),
    path('order-placed/<str:order_id>/<str:payment_id>/<str:order_status_id>',v.order_placed,name='order_placed'),
    path('order-deatails',v.order_deatails,name='order_deatails'),
    
    path('cancel-order',v.cancel_order,name='cancel_order'),
    path('search-order',v.search_order,name='search_order'),
    path('filter-orders',v.filter_orders,name='filter_orders'),
    path('order-placed-history/orderid=<str:id>&<int:orderpk>&itemid=<int:itemid>&statusid=<int:sid>&payment-id=<int:payid>',v.order_placed_history,name='order_placed_history'),
    
    path('razorpay-payment/<str:product_order_id>/',r.razorpay_payment,name='razorpay_payment'),
    path('paypal',p.paypal,name='paypal'),
    
    path('invoice&order_id=<int:order_id>&order_status=<int:orderstatus>',i.invoice,name='invoice'),
    
    path('refund-list',re.refund_list,name='refund_list'),
    
    path('cancel-resons',cr.cancel_resons,name='cancel_resons'),
    path('add-cancel',cr.add_cancel,name='add_cancel'),
    path('cancel-is-active',cr.cancel_is_active,name='cancel_is_active'),
    path('cencel-delete',cr.cencel_delete,name='cencel_delete'),
    path('edit-cancel',cr.edit_cancel,name='edit_cancel'),
    
    path('cash-on-delivery-text',ct.cash_on_delivery_text,name='cash_on_delivery_text'),
    path('add_cash_on_delivery_text',ct.add_cash_on_delivery_text,name='add_cash_on_delivery_text'),
    path('cash_on_delivery_text_is_active',ct.cash_on_delivery_text_is_active,name='cash_on_delivery_text_is_active'),
    path('cash_on_delivery_text_delete',ct.cash_on_delivery_text_delete,name='cash_on_delivery_text_delete'),
    path('edit_cash_on_delivery_text',ct.edit_cash_on_delivery_text,name='edit_cash_on_delivery_text'),
    
         
]
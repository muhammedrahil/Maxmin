from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from cart.models import *
from .models import *

def invoice(request,*args,**kwargs):
    order_id=kwargs.get('order_id')
    orderstatus=kwargs.get('orderstatus')
    order_instence=get_object_or_404(Order,pk=order_id,order_status='ordered',is_active=True)
    orderstatus=get_object_or_404(OrderStatus,pk=orderstatus,is_active=True)
    payment=get_object_or_404(Payment,order=order_instence,is_active=True,user=request.user)
    
    return render(request,'user/payment-order/order-placed-history/invoice.html',{'order':order_instence,'Payment':payment})


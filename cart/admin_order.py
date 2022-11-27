from django.utils import timezone
from django.shortcuts import render,get_object_or_404,redirect
from .models import Order,OrderStatus as OrderStatusModel
from payment.models import Payment
from django.contrib.sites.shortcuts import get_current_site
import base64
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required(login_url='accounts:maxmin_admin')
def order(request,*args,**kwargs):
  try:
    order_list=Payment.objects.select_related('order_status','order_status__order').filter(order_status__order__is_active=True).order_by('-order_status__order__order_date')
    context={
      'order_list':order_list,
      'current_site':str(get_current_site(request))
    }
    return render(request,'admin_/order/order.html',context)
  except:
    return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def order_deatails(request,*args,**kwargs):
  try:
    pay_id=kwargs.get('pay_id')
    status_id=kwargs.get('status_id')
    order_id=kwargs.get('order_id')
    
    pay_id_denc=base64.b64decode(pay_id)
    pay_id = pay_id_denc.decode('ascii')

    status_id_denc=base64.b64decode(status_id)
    status_id = status_id_denc.decode('ascii')

    order_id_denc=base64.b64decode(order_id)
    order_id = order_id_denc.decode('ascii')
    
    payment_instence=get_object_or_404(Payment,pk=pay_id)
    order_status_instence=get_object_or_404(OrderStatusModel,pk=status_id)
    order_instence=get_object_or_404(Order,pk=order_id)
    context={
      'payment_instence':payment_instence,
      'order_status_instence':order_status_instence,
      'order_instence':order_instence
    }
    
    return render(request,'admin_/order/order-deatails/order-deatails.html',context)
  except:
    return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def update_status(request,*args,**kwargs):
  pk=kwargs.get('pk')
  if request.method == 'POST':
    order_status_instence=get_object_or_404(OrderStatusModel,pk=pk)
    order_confirmed=request.POST.get('order_confirmed',None)
    Shipped=request.POST.get('Shipped',None)
    out_for_delivery=request.POST.get('out_for_delivery',None)
    delivered=request.POST.get('delivered',None)
    if order_confirmed != None:
      order_status_instence.order_confirmed=True
      order_status_instence.order_confirmed_date=timezone.now()
    if Shipped != None:
      order_status_instence.Shipped=True
      order_status_instence.Shipped_date=timezone.now()
    if out_for_delivery != None:
      order_status_instence.Shipped=True
      order_status_instence.Shipped_date=timezone.now()
      order_status_instence.out_for_delivery=True
      order_status_instence.out_for_delivery_date=timezone.now()
    if delivered != None:
      order_status_instence.Shipped=True
      order_status_instence.Shipped_date=timezone.now()
      order_status_instence.out_for_delivery=True
      order_status_instence.out_for_delivery_date=timezone.now()
      order_status_instence.delivered=True
      order_status_instence.delivered_date=timezone.now()
    order_status_instence.save()
  return redirect('cart:order')
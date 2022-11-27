from django.shortcuts import redirect, render,get_object_or_404
# from cart.order import get_client_ip
from cart.models import OrderStatus

from django.http import JsonResponse
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


def  sales_report(request,*args,**kwargs):
  try:
    order=OrderStatus.objects.select_related('order').filter(order__is_active=True).exclude(Cancelled=True)
    return render(request,'admin_/sales/sales.html',{'order':order})
  except:
    return render(request,'massages/404.html')
  
def date_filter(request,*args,**kwargs):
  try:
    if request.method == 'POST':
      date1=request.POST.get('date1',None)
      date2=request.POST.get('date2',None)  
      order=OrderStatus.objects.select_related('order').filter(order__is_active=True).exclude(Cancelled=True)
      if len(date1) != 0:
        order=order.filter(order__order_date__gte=date1)
      if len(date2) != 0:
        order=order.filter(order__order_date__lte=date2)
      return render(request,'admin_/sales/sales.html',{'order':order})
  except:
    return render(request,'massages/404.html')
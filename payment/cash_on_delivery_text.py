from django.shortcuts import render,get_object_or_404
from .models import CashOnDeliveryTextGenarator
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='accounts:maxmin_admin')
def cash_on_delivery_text(request,*args,**kwargs):
  try:
    cash_on_delivery_text=CashOnDeliveryTextGenarator.objects.all()
    context={
      'cash_on_delivery_text':cash_on_delivery_text
    }
    return render(request,'admin_/cash_on_delivery_text/cash_on_delivery_text.html',context)
  except:
    return render(request,'massages/404.html')
  
@staff_member_required(login_url='accounts:maxmin_admin')
def add_cash_on_delivery_text(request,*args,**kwargs):
  cash_on_delivery_text=request.POST.get('cash_on_delivery_text',None)
  cash_on_delivery=CashOnDeliveryTextGenarator()
  cash_on_delivery.text=cash_on_delivery_text
  cash_on_delivery.save()
  return JsonResponse({'data':True}) 


@staff_member_required(login_url='accounts:maxmin_admin')
def cash_on_delivery_text_is_active(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    cash_on_delivery=get_object_or_404(CashOnDeliveryTextGenarator,pk=pk)
    if cash_on_delivery.is_active == False:
        cash_on_delivery.is_active = True
        status=True
    else:
        cash_on_delivery.is_active = False
        status = False
    cash_on_delivery.save()
    return JsonResponse({'data':status})
  
  
@staff_member_required(login_url='accounts:maxmin_admin')
def cash_on_delivery_text_delete(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    cash_on_delivery=get_object_or_404(CashOnDeliveryTextGenarator,pk=pk)
    cash_on_delivery.delete()
    return JsonResponse({'data':True})
  
@staff_member_required(login_url='accounts:maxmin_admin')
def edit_cash_on_delivery_text(request,*args,**kwargs):
  if request.method == 'POST':
    pk=request.POST.get('pk', None)
    cash_on_delivery_text=request.POST.get('cash_on_delivery_text',None)
    cash_on_delivery=get_object_or_404(CashOnDeliveryTextGenarator,pk=pk)
    cash_on_delivery.text=cash_on_delivery_text
    cash_on_delivery.save()
    return JsonResponse({'data':True})
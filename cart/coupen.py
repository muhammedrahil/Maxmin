from django.shortcuts import render,get_object_or_404,redirect
from .models import Coupon
from cart.order import get_client_ip
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required(login_url='accounts:maxmin_admin')
def coupen_list(request,*args,**kwargs):
  try:
    coupen_list=Coupon.objects.exclude(record_status='deleted').order_by('-created_date')
    context={
      'coupen_list':coupen_list
    }
    return render(request,'admin_/coupen/coupen.html',context)
  except:
    return render(request,'massages/404.html')



@staff_member_required(login_url='accounts:maxmin_admin')
def add_coupen(request,*args,**kwargs):
  try:
    coupen_text=request.POST.get('coupen_text',None)
    coupen_expiry_date=request.POST.get('coupen_expiry_date',None)
    offer_persentage=request.POST.get('offer_persentage',None)
    graiter_price=request.POST.get('graiter_price',None)
    if Coupon.objects.filter(coupon__exact=coupen_text,is_active=True).exists():
      return JsonResponse({'data':False})   
    coupen=Coupon()
    coupen.coupon=coupen_text
    coupen.expiry_date=coupen_expiry_date
    coupen.persentage_off=float(offer_persentage)
    coupen.gtr_price=graiter_price
    coupen.created_id=request.user
    coupen.created_ip=get_client_ip(request)
    coupen.save()
    return JsonResponse({'data':True})
  except:
    return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def coupen_is_active(request,*args,**kwargs):
  try:
      pk=request.POST.get('pk', None)
      coupen=get_object_or_404(Coupon,pk=pk)
      coupen.modified_id=request.user
      coupen.modified_ip=get_client_ip(request)
      coupen.record_status='modified'
      if coupen.is_active == False:
          coupen.is_active = True
          status=True
      else:
          coupen.is_active = False
          status = False
      coupen.save()
      return JsonResponse({'data':status})
  except:
    return render(request,'massages/404.html')
  
@staff_member_required(login_url='accounts:maxmin_admin')
def coupen_delete(request,*args,**kwargs):
  try:
    pk=request.POST.get('pk', None)
    coupen=get_object_or_404(Coupon,pk=pk)
    coupen.modified_id=request.user
    coupen.modified_ip=get_client_ip(request)
    coupen.record_status='deleted'
    coupen.is_active=False
    coupen.save()
    return JsonResponse({'data':True})
  except:
    return render(request,'massages/404.html')
  
  
@staff_member_required(login_url='accounts:maxmin_admin') 
def edit_coupen(request,*args,**kwargs):
  try:
    if request.method == 'POST':
      pk=request.POST.get('pk', None)
      coupen_text=request.POST.get('coupen_text',None)
      coupen_expiry_date=request.POST.get('coupen_expiry_date',None)
      offer_persentage=request.POST.get('offer_persentage',None)
      graiter_price=request.POST.get('graiter_price',None)
      coupen=get_object_or_404(Coupon,pk=pk)
      if coupen.coupon != coupen_text:
        if Coupon.objects.filter(coupon__exact=coupen_text,is_active=True).exists():
          return JsonResponse({'data':False})   
      coupen.coupon=coupen_text
      coupen.expiry_date=coupen_expiry_date
      coupen.persentage_off=float(offer_persentage)
      coupen.gtr_price=graiter_price
      coupen.modified_id=request.user
      coupen.modified_ip=get_client_ip(request)
      coupen.record_status='modified'
      coupen.save()
      return JsonResponse({'data':True})
  except:
    return JsonResponse({'data':False})
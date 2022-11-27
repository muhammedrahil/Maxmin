from django.shortcuts import render,get_object_or_404
from cart.models import CancelReasons
from django.http import JsonResponse
from cart.order import get_client_ip
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='accounts:maxmin_admin')
def cancel_resons(request,*args,**kwargs):
  try:
    cancel_resons=CancelReasons.objects.exclude(record_status='deleted')
    context={
      'cancel_resons':cancel_resons
    }
    return render(request,'admin_/cancel/cancel.html',context)
  except:
    return render(request,'massages/404.html')
  
@staff_member_required(login_url='accounts:maxmin_admin')
def add_cancel(request,*args,**kwargs):
  resons_text=request.POST.get('resons_text',None)
  cancel=CancelReasons()
  cancel.reasons=resons_text
  cancel.created_id=request.user
  cancel.created_ip=get_client_ip(request)
  cancel.save()
  return JsonResponse({'data':True}) 


@staff_member_required(login_url='accounts:maxmin_admin')
def cancel_is_active(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    cancel=get_object_or_404(CancelReasons,pk=pk)
    cancel.modified_id=request.user
    cancel.modified_ip=get_client_ip(request)
    cancel.record_status='modified'
    if cancel.is_active == False:
        cancel.is_active = True
        status=True
    else:
        cancel.is_active = False
        status = False
    cancel.save()
    return JsonResponse({'data':status})
  
  
@staff_member_required(login_url='accounts:maxmin_admin')
def cencel_delete(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    cancel=get_object_or_404(CancelReasons,pk=pk)
    cancel.modified_id=request.user
    cancel.modified_ip=get_client_ip(request)
    cancel.record_status='deleted'
    cancel.is_active=False
    cancel.save()
    return JsonResponse({'data':True})
  
@staff_member_required(login_url='accounts:maxmin_admin')
def edit_cancel(request,*args,**kwargs):
  if request.method == 'POST':
    pk=request.POST.get('pk', None)
    resons_text=request.POST.get('resons_text',None)
    cancel=get_object_or_404(CancelReasons,pk=pk)
    cancel.reasons=resons_text
    cancel.modified_id=request.user
    cancel.modified_ip=get_client_ip(request)
    cancel.record_status='modified'
    cancel.save()
    return JsonResponse({'data':True})
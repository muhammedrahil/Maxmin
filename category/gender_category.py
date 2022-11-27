from django.shortcuts import render,get_object_or_404
from .models import GenderCategory
from django.http import JsonResponse
from cart.order import get_client_ip
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required(login_url='accounts:maxmin_admin')
def gender_category(request,*args,**kwargs):
  try:
    gender_category=GenderCategory.objects.exclude(record_status='deleted')
    context={
      'gender_category':gender_category
    }
    return render(request,'admin_/gender_category/gender_category.html',context)
  except:
    return render(request,'massages/404.html')


@staff_member_required(login_url='accounts:maxmin_admin')
def add_gender_category(request,*args,**kwargs):
  gender_category_text=request.POST.get('gender_category',None)
  gender_category=GenderCategory()
  gender_category.gender=gender_category_text
  gender_category.created_id=request.user
  gender_category.created_ip=get_client_ip(request)
  gender_category.save()
  return JsonResponse({'data':True}) 


@staff_member_required(login_url='accounts:maxmin_admin')
def gender_category_is_active(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    gender_category=get_object_or_404(GenderCategory,pk=pk)
    gender_category.modified_id=request.user
    gender_category.modified_ip=get_client_ip(request)
    gender_category.record_status='modified'
    if gender_category.is_active == False:
        gender_category.is_active = True
        status=True
    else:
        gender_category.is_active = False
        status = False
    gender_category.save()
    return JsonResponse({'data':status})
  
  
@staff_member_required(login_url='accounts:maxmin_admin')
def gender_category_delete(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    gender_category=get_object_or_404(GenderCategory,pk=pk)
    gender_category.modified_id=request.user
    gender_category.modified_ip=get_client_ip(request)
    gender_category.record_status='deleted'
    gender_category.is_active=False
    gender_category.save()
    return JsonResponse({'data':True})
  
@staff_member_required(login_url='accounts:maxmin_admin')  
def edit_gender_category(request,*args,**kwargs):
  if request.method == 'POST':
    pk=request.POST.get('pk', None)
    gender_category_text=request.POST.get('gender_category',None)
    gender_category=get_object_or_404(GenderCategory,pk=pk)
    gender_category.gender=gender_category_text
    gender_category.modified_id=request.user
    gender_category.modified_ip=get_client_ip(request)
    gender_category.record_status='modified'
    gender_category.save()
    return JsonResponse({'data':True})
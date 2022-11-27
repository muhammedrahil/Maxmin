
from django.shortcuts import redirect, render,get_object_or_404
from .models import Product as Products,SubProductAttribute 
from .models import Advertisement
from cart.order import get_client_ip
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def product_list(request):
    product_list=Products.objects.exclude(record_status='deleted').order_by('-created_date')
    return product_list


@staff_member_required(login_url='accounts:maxmin_admin')
def banner(request,*args,**kwargs):
  try:
    context={
      'product_list': product_list(request),
      'banner_list': Advertisement.objects.exclude(record_status='deleted').order_by('-created_date')
    }
    return render(request,'admin_/banner/banner.html',context)
  except:
    return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def add_banner(request,*args,**kwargs):
  pk=kwargs.get('pk')
  if request.method == 'POST':
    advertisement=Advertisement()
    banner=request.POST.get('banner')
    if request.FILES.get('banner_image') != None:
          banner_image=request.FILES.get('banner_image')
          advertisement.banner=banner_image
    product=get_object_or_404(Products,pk=pk)
    advertisement.product=product
    if banner == '1':
      advertisement.hero_banner=True
    if banner == '2':
      advertisement.mainbanner=True
    if banner == '3':
      advertisement.centerbanner=True
    if banner == '4':
      advertisement.small_banner=True
    advertisement.created_id=request.user
    advertisement.created_ip=get_client_ip(request)
    advertisement.save() 
    return redirect('landing:banner')


@staff_member_required(login_url='accounts:maxmin_admin')
def change_banner(request,*args,**kwargs):
  pk = request.POST.get('pk')
  adv_product=get_object_or_404(Advertisement,pk=pk)
  if request.FILES.get('change_img') != None:
    change_img=request.FILES.get('change_img')
    adv_product.banner=change_img
  adv_product.modified_id=request.user
  adv_product.modified_ip=get_client_ip(request)
  adv_product.record_status='modified'
  adv_product.save()
  return JsonResponse({'data':True})

@staff_member_required(login_url='accounts:maxmin_admin')
def active_banner(request,*args,**kwargs):
  pk = request.POST.get('pk')
  adv_product=get_object_or_404(Advertisement,pk=pk)
  if adv_product.is_active == True:
    adv_product.is_active = False
    status=False
  else:
    adv_product.is_active = True
    status=True
  adv_product.modified_id=request.user
  adv_product.modified_ip=get_client_ip(request)
  adv_product.record_status='modified'
  adv_product.save()
  return JsonResponse({'data':status})

@staff_member_required(login_url='accounts:maxmin_admin')
def edit_banner(request,*args,**kwargs):
  pk =kwargs.get('pk')
  if request.method == 'POST':
    banner=request.POST.get('banner')
    advertisement=get_object_or_404(Advertisement,pk=pk)
    if advertisement.hero_banner == True:
      advertisement.hero_banner=False
    if advertisement.mainbanner == True:
      advertisement.mainbanner=False
    if advertisement.centerbanner == True:
      advertisement.centerbanner=False
    if advertisement.small_banner == True:
      advertisement.small_banner=False
    if banner == '1':
      advertisement.hero_banner=True
    if banner == '2':
      advertisement.mainbanner=True
    if banner == '3':
      advertisement.centerbanner=True
    if banner == '4':
      advertisement.small_banner=True
    advertisement.modified_id=request.user
    advertisement.modified_ip=get_client_ip(request)
    advertisement.record_status='modified'
    advertisement.save() 
  return redirect('landing:banner') 

@staff_member_required(login_url='accounts:maxmin_admin')
def banner_delete_product(request,*args,**kwargs):
  pk = request.POST.get('pk')
  adv_product=get_object_or_404(Advertisement,pk=pk)
  adv_product.is_active=False
  adv_product.modified_id=request.user
  adv_product.modified_ip=get_client_ip(request)
  adv_product.record_status='deleted'
  adv_product.save()
  return JsonResponse({'data':True}) 
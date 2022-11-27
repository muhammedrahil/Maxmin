from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from category.models import GenderCategory,Brand,Category as CategoryModel
from .models import Product as Products,SubProductAttribute 
from cart.order import get_client_ip
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.admin.views.decorators import staff_member_required
from category.admin_category import category_list


def product_list(request):
    product_list=Products.objects.exclude(record_status='deleted').order_by('-created_date')
    return product_list

# Create your views here.
@staff_member_required(login_url='accounts:maxmin_admin')
def admin_product(request,*args,**kwargs):
    try:
        category=category_list(request)
        context={
            'gender':GenderCategory.objects.filter(is_active=True),
            'brand': Brand.objects.filter(is_active=True),
            'category': category,
            'product_list': product_list(request),
            'current_site': str(get_current_site(request))
        }
        return render(request, 'admin_/products/all-product.html',context)
    except:
        return render(request,'massages/404.html')



@staff_member_required(login_url='accounts:maxmin_admin')
def add_product(request,*args,**kwargs):
    # print(request.POST,request.FILES)
    gender_category=request.POST.getlist('gender_category')
    product_name=request.POST.get('product_name')
    unit_price=request.POST.get('unit_price')
    product_caregory=request.POST.get('product_caregory')
    product_brand=request.POST.get('product_brand')
    description=request.POST.get('description')
    product_instence=Products()
    product_category_instence=get_object_or_404(CategoryModel,pk=product_caregory)
    product_instence.category=product_category_instence
    product_brand_instence=get_object_or_404(Brand,pk=product_brand)
    product_instence.product_brand=product_brand_instence
    product_instence.product_name=product_name
    product_instence.unit_price=float(unit_price)
    if request.FILES.get('product_image') != None:
        product_image=request.FILES.get('product_image')
        product_instence.main_image=product_image
    product_instence.description=description
    product_instence.created_id=request.user
    product_instence.created_ip=get_client_ip(request)
    product_instence.save()
    for i in gender_category:
        product_instence.main_category.add(i)
    pk=product_instence.pk
    return JsonResponse({'data':True,'pk':pk})



@staff_member_required(login_url='accounts:maxmin_admin')
def edit_product(request,*args,**kwargs):
    # print(request.POST)
    pk=request.POST.get('pk', None)
    gender_category=request.POST.getlist('data[gender_category][]')
    product_name=request.POST.getlist('data[product_name]')
    unit_price=request.POST.getlist('data[unit_price]')
    product_caregory=request.POST.getlist('data[product_caregory]')
    product_brand=request.POST.getlist('data[product_brand]')
    description=request.POST.getlist('data[description]')
    product_instence=get_object_or_404(Products,pk=pk)
    product_category_instence=get_object_or_404(CategoryModel,pk=product_caregory[0])
    product_instence.category=product_category_instence
    product_brand_instence=get_object_or_404(Brand,pk=product_brand[0])
    product_instence.product_brand=product_brand_instence
    product_instence.product_name=product_name[0]
    product_instence.unit_price=float(unit_price[0])
    product_instence.description=description[0]
    product_instence.modified_id=request.user
    product_instence.modified_ip=get_client_ip(request)
    product_instence.record_status='modified'
    product_instence.save()
    product_instence.main_category.clear() 
    for i in gender_category:
        product_instence.main_category.add(i)  
    return JsonResponse({'data':True})


@staff_member_required(login_url='accounts:maxmin_admin')
def product_active(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    product_instence=get_object_or_404(Products,pk=pk)
    product_instence.modified_id=request.user
    product_instence.modified_ip=get_client_ip(request)
    product_instence.record_status='modified'
    sub_products=SubProductAttribute.objects.filter(product=product_instence)
    if product_instence.is_active == False:
        product_instence.is_active = True
        for s in sub_products:
            s.is_active=True
            s.modified_id=request.user
            s.modified_ip=get_client_ip(request)
            s.record_status='modified'
            s.save()
        status=True
    else:
        product_instence.is_active = False
        for s in sub_products:
            s.is_active=False
            s.modified_id=request.user
            s.modified_ip=get_client_ip(request)
            s.record_status='modified'
            s.save()
        status = False
    product_instence.save()
    return JsonResponse({'data':status})

@staff_member_required(login_url='accounts:maxmin_admin')
def delete_product(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    product_instence=get_object_or_404(Products,pk=pk)
    product_instence.modified_id=request.user
    product_instence.modified_ip=get_client_ip(request)
    product_instence.record_status='deleted'
    product_instence.is_active = False
    product_instence.save()
    sub_products=SubProductAttribute.objects.filter(product=product_instence)
    for s in sub_products:
        s.is_active=False
        s.modified_id=request.user
        s.modified_ip=get_client_ip(request)
        s.record_status='deleted'
        s.save()
    status = True
    return JsonResponse({'data':status})


@staff_member_required(login_url='accounts:maxmin_admin')
def change_image_product(request,*args,**kwargs):   
    try:
        pk = request.POST.get('pk',None)
        product_instence=get_object_or_404(Products,pk=pk)
        if request.FILES.get('change_img') != None:
            change_img=request.FILES.get('change_img')
            product_instence.main_image=change_img
        product_instence.modified_id=request.user
        product_instence.modified_ip=get_client_ip(request)
        product_instence.record_status='modified'
        product_instence.save()
        status=True
    except:
        status=False
    return JsonResponse({'data':status})
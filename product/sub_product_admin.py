import base64
from django.shortcuts import redirect, render,get_object_or_404
from .models import Product as Products,SubProductAttribute,ProductQuantity
from category.models import Color,Size
from cart.order import get_client_ip
import decimal 
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

@staff_member_required(login_url='accounts:maxmin_admin')
def sub_product(request,*args,**kwargs):
        try:
                pk=kwargs.get('pk')
                denc = base64.b64decode(pk)
                pk = denc.decode('ascii')
                product=get_object_or_404(Products,pk=pk) 
                        
                context={
                        'product':product,
                        'color': Color.objects.filter(is_active=True),
                        'sub_products':SubProductAttribute.objects.exclude(record_status='deleted').filter(product=product),
                        'current_site': str(get_current_site(request))
                }
                return render(request,'admin_/products/sub-product/sub-product.html',context)
        except:
                return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def add_sub_product(request,*args,**kwargs):
        try:
                pk=kwargs.get('pk')
                product=get_object_or_404(Products,pk=pk) 
                if request.method == 'POST' and request.FILES:        
                        sku=request.POST['sub_product_sku']
                        offer_price=request.POST['sub_product_offer_price']
                        colors=request.POST['sub_product_colors']
                        expiry_date=request.POST['sub_product_offer_expiry_date']       
                        subProduct_attribute_instence=SubProductAttribute()
                        subProduct_attribute_instence.product=product
                        subProduct_attribute_instence.sku=sku
                        color=get_object_or_404(Color,pk=colors)
                        subProduct_attribute_instence.product_color=color
                        subProduct_attribute_instence.offerprice=decimal.Decimal(offer_price)
                        subProduct_attribute_instence.offer_expiry_date=expiry_date
                        subProduct_attribute_instence.created_id=request.user
                        subProduct_attribute_instence.created_ip=get_client_ip(request)
                        
                        if  request.FILES.get('subproductimage1') != None:
                                subproductimage1=request.FILES.get('subproductimage1',None)
                                subProduct_attribute_instence.images=subproductimage1
                        if  request.FILES.get('subproductimage2')!= None:
                                subproductimage2=request.FILES.get('subproductimage2',None)
                                subProduct_attribute_instence.images2=subproductimage2                
                        if request.FILES.get('subproductimage3') != None :
                                subproductimage3=request.FILES.get('subproductimage3',None)
                                subProduct_attribute_instence.images3=subproductimage3
                        if request.FILES.get('subproductimage4') != None:
                                subproductimage4=request.FILES.get('subproductimage4',None)
                                subProduct_attribute_instence.images4=subproductimage4
                        if request.FILES.get('subproductimage5') != None:
                                subproductimage5=request.FILES.get('subproductimage5',None)
                                subProduct_attribute_instence.images5=subproductimage5
                        if request.FILES.get('subproductimage6') != None:
                                subproductimage6=request.FILES.get('subproductimage6',None)
                                subProduct_attribute_instence.images6=subproductimage6
                        subProduct_attribute_instence.save()
                        
                        enc = base64.b64encode(str(pk).encode('ascii'))
                        enc=enc.decode()
                        sub_pkenc = base64.b64encode(str(subProduct_attribute_instence.pk).encode('ascii'))
                        sub_pkenc=sub_pkenc.decode()
                        return redirect('product:add_sub_product_qauntity',pk=enc,sub_pk=sub_pkenc)
        except:
              return  HttpResponse("<script>alert('Sku already Exists , Add another Sku Units');window.history.back()</script>")
      
@staff_member_required(login_url='accounts:maxmin_admin')
def edit_sub_product(request,*args,**kwargs):
        try:
                pk=kwargs.get('pk')
                denc = base64.b64decode(pk)
                pk = denc.decode('ascii')
                sub_product_attr=get_object_or_404(SubProductAttribute,pk=pk)
                context={
                        'sub_prod':sub_product_attr,
                        'color': Color.objects.filter(is_active=True),
                }
                return render(request,'admin_/products/sub-product/edit/edit-page.html',context)
        except:
                return render(request,'massages/404.html')
        
        
        
@staff_member_required(login_url='accounts:maxmin_admin')
def edit_sub_product_form(request,*args,**kwargs):
        pk=kwargs.get('sub_pk')
        print(request.POST,request.FILES)
        try:
                if request.method == 'POST':        
                        sku=request.POST['sub_product_sku']
                        offer_price=request.POST['sub_product_offer_price']
                        colors=request.POST['sub_product_colors']
                        expiry_date=request.POST['sub_product_offer_expiry_date']       
                        subProduct_attribute_instence=get_object_or_404(SubProductAttribute,pk=pk)
                        subProduct_attribute_instence.sku=sku
                        color=get_object_or_404(Color,pk=colors)
                        subProduct_attribute_instence.product_color=color
                        subProduct_attribute_instence.offerprice=decimal.Decimal(offer_price)
                        subProduct_attribute_instence.offer_expiry_date=expiry_date
                        subProduct_attribute_instence.modified_id=request.user
                        subProduct_attribute_instence.modified_ip=get_client_ip(request)
                        subProduct_attribute_instence.record_status='modified'
                        if  request.FILES.get('subproductimage1') != None:
                                print('safhvbfh')
                                subproductimage1=request.FILES.get('subproductimage1',None)
                                subProduct_attribute_instence.images=subproductimage1
                        if  request.FILES.get('subproductimage2')!= None:
                                subproductimage2=request.FILES.get('subproductimage2',None)
                                subProduct_attribute_instence.images2=subproductimage2                
                        if request.FILES.get('subproductimage3') != None :
                                subproductimage3=request.FILES.get('subproductimage3',None)
                                subProduct_attribute_instence.images3=subproductimage3
                        if request.FILES.get('subproductimage4') != None:
                                subproductimage4=request.FILES.get('subproductimage4',None)
                                subProduct_attribute_instence.images4=subproductimage4
                        if request.FILES.get('subproductimage5') != None:
                                subproductimage5=request.FILES.get('subproductimage5',None)
                                subProduct_attribute_instence.images5=subproductimage5
                        if request.FILES.get('subproductimage6') != None:
                                subproductimage6=request.FILES.get('subproductimage6',None)
                                subProduct_attribute_instence.images6=subproductimage6
                        subProduct_attribute_instence.save()
                        product_order_id=str(subProduct_attribute_instence.product.pk)
                        enc = base64.b64encode(product_order_id.encode('ascii'))
                        enc=enc.decode()
                        return redirect('product:sub_product',pk=enc)
        except:
              return  HttpResponse("<script>alert('Sku already Exists , Add another Sku Units');window.history.back()</script>")
@staff_member_required(login_url='accounts:maxmin_admin')
def sub_product_active(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    subproduct_instence=get_object_or_404(SubProductAttribute,pk=pk)
    subproduct_instence.modified_id=request.user
    subproduct_instence.modified_ip=get_client_ip(request)
    subproduct_instence.record_status='modified'
    sub_qty_products=ProductQuantity.objects.filter(product=subproduct_instence)
    if subproduct_instence.is_active == False:
        subproduct_instence.is_active = True
        for s in sub_qty_products:
            s.is_active=True
            s.modified_id=request.user
            s.modified_ip=get_client_ip(request)
            s.record_status='modified'
            s.save()
        status=True
    else:
        subproduct_instence.is_active = False
        for s in sub_qty_products:
            s.is_active=False
            s.modified_id=request.user
            s.modified_ip=get_client_ip(request)
            s.record_status='modified'
            s.save()
        status = False
    subproduct_instence.save()
    return JsonResponse({'data':status})

@staff_member_required(login_url='accounts:maxmin_admin')
def sub_delete_product(request,*args,**kwargs):
    pk=request.POST.get('pk', None)
    subproduct_instence=get_object_or_404(SubProductAttribute,pk=pk)
    subproduct_instence.modified_id=request.user
    subproduct_instence.modified_ip=get_client_ip(request)
    subproduct_instence.record_status='deleted'
    subproduct_instence.is_active=False
    subproduct_instence.save()
    sub_qty_products=ProductQuantity.objects.filter(product=subproduct_instence)
    for s in sub_qty_products:
        s.is_active=False
        s.modified_id=request.user
        s.modified_ip=get_client_ip(request)
        s.record_status='deleted'
        s.save()
    status = True
    return JsonResponse({'data':status})



import base64
from django.shortcuts import  render,get_object_or_404
from .models import Product as Products,SubProductAttribute,ProductQuantity
from category.models import Size
from cart.order import get_client_ip
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='accounts:maxmin_admin')       
def add_sub_product_qauntity(request,*args,**kwargs):
        try:
                pk=kwargs.get('pk')
                sub_pk=kwargs.get('sub_pk')
                product_denc = base64.b64decode(pk)
                pk = product_denc.decode('ascii')
                product=get_object_or_404(Products,pk=pk) 
                sub_product_denc=base64.b64decode(sub_pk)
                sub_pk = sub_product_denc.decode('ascii')
                sub_product=get_object_or_404(SubProductAttribute,pk=sub_pk)
                context={
                        'sub_product':sub_product,
                        'size':Size.objects.filter(category=product.category.parent,is_active=True),
                        'size_qauntity':ProductQuantity.objects.filter(product=sub_product,product__is_active=True,is_active=True)
                }
                return render(request,'admin_/products/sub-product/quantity/size-quantity.html',context)
        except:
                return render(request,'massages/404.html')

@staff_member_required(login_url='accounts:maxmin_admin')
def add_size_quantity(request,*args,**kwargs):
        if request.method == 'POST':
                size_id=request.POST.get('id_sub_size')
                quantity=request.POST.get('add_sub_qauntity')
                sub_product_id=request.POST.get('subproduct_id')
                sub_product_instence=get_object_or_404(SubProductAttribute,pk=sub_product_id)
                size=get_object_or_404(Size,pk=size_id)
                quantity_instence=ProductQuantity()
                quantity_instence.product=sub_product_instence
                quantity_instence.product_size=size
                quantity_instence.quantity=quantity
                quantity_instence.stock=quantity
                quantity_instence.created_id=request.user
                quantity_instence.created_ip=get_client_ip(request)
                quantity_instence.save()
                
                sub_product_instence.sub_product_totel_stoke+=int(quantity_instence.stock)
                sub_product_instence.modified_id=request.user
                sub_product_instence.modified_ip=get_client_ip(request)
                sub_product_instence.record_status='modified'
                sub_product_instence.save()
                
                product_instence=get_object_or_404(Products,pk=sub_product_instence.product.pk)
                product_instence.product_totel_stoke+=int(quantity_instence.stock)
                product_instence.modified_id=request.user
                product_instence.modified_ip=get_client_ip(request)
                product_instence.record_status='modified'
                product_instence.save()
                return JsonResponse({'data':True,})

@staff_member_required(login_url='accounts:maxmin_admin')
def edit_size_quantity(request,*args,**kwargs):
        if request.method == 'POST':
                size_id=request.POST.get('id_sub_size')
                quantity=request.POST.get('add_sub_qauntity')
                pk=request.POST.get('pk')
                product_qty_instence=get_object_or_404(ProductQuantity,pk=pk)
                size=get_object_or_404(Size,pk=size_id)
                product_qty_instence.product_size=size
                product_qty_instence.quantity=quantity
                edit_amt=int(quantity)-int(product_qty_instence.stock)
                product_qty_instence.stock+=edit_amt
                product_qty_instence.modified_id=request.user
                product_qty_instence.modified_ip=get_client_ip(request)
                product_qty_instence.record_status='modified'
                product_qty_instence.save()
                
                sub_product_instence=get_object_or_404(SubProductAttribute,pk=product_qty_instence.product.pk)
                sub_product_instence.sub_product_totel_stoke+=edit_amt
                sub_product_instence.modified_id=request.user
                sub_product_instence.modified_ip=get_client_ip(request)
                sub_product_instence.record_status='modified'
                sub_product_instence.save()
                
                product_instence=get_object_or_404(Products,pk=sub_product_instence.product.pk)
                product_instence.product_totel_stoke+=edit_amt
                product_instence.modified_id=request.user
                product_instence.modified_ip=get_client_ip(request)
                product_instence.record_status='modified'
                product_instence.save()
                return JsonResponse({'data':True,})
        
@staff_member_required(login_url='accounts:maxmin_admin')
def delete_size_qty(request,*args,**kwargs):
        pk=request.POST.get('pk')
        product_qty_instence=get_object_or_404(ProductQuantity,pk=pk)
        product_qty_instence.is_active=False
        product_qty_instence.modified_id=request.user
        product_qty_instence.modified_ip=get_client_ip(request)
        product_qty_instence.record_status='deleted'
        product_qty_instence.save()
        
        sub_product_instence=get_object_or_404(SubProductAttribute,pk=product_qty_instence.product.pk)
        sub_product_instence.sub_product_totel_stoke-=product_qty_instence.stock
        sub_product_instence.modified_id=request.user
        sub_product_instence.modified_ip=get_client_ip(request)
        sub_product_instence.record_status='modified'
        sub_product_instence.save()
        
        product_instence=get_object_or_404(Products,pk=sub_product_instence.product.pk)
        product_instence.product_totel_stoke-=product_qty_instence.stock
        product_instence.modified_id=request.user
        product_instence.modified_ip=get_client_ip(request)
        product_instence.record_status='modified'
        product_instence.save()
        return JsonResponse({'data':True,})
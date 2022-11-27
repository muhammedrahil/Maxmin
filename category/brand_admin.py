from django.shortcuts import get_object_or_404,redirect
from django.views.generic import ListView
from .models import Brand as BrandModel,Category as CategoryModel
from cart.order import get_client_ip
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@method_decorator(staff_member_required(login_url='accounts:maxmin_admin'),name='dispatch')
class Brand(ListView):
    model=BrandModel
    template_name = 'admin_/categories/brand/brand.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['brand'] = BrandModel.objects.exclude(record_status='deleted')
        context['category'] = CategoryModel.objects.filter(is_active=True).filter(level=0)
        return context

@staff_member_required(login_url='accounts:maxmin_admin') 
def add_brand(request,*args,**kwargs):
    if request.method == 'POST' :
        brand_instence=BrandModel()
        brand_name=request.POST['brand_name']
        brand_description=request.POST['description']
        if len(request.FILES)!=0:
            brand_image=request.FILES['image_brand']
            brand_instence.brand_images=brand_image
        category=request.POST.getlist('brand_category')
        brand_instence.title=brand_name
        brand_instence.discription=brand_description
        brand_instence.created_id=request.user
        brand_instence.created_ip=get_client_ip(request)
        brand_instence.save()
        for i in category:
            brand_instence.brand_category.add(i)
        return redirect('category:brand')
    
@staff_member_required(login_url='accounts:maxmin_admin')
def edit_brand(request,*args,**kwargs):
    if request.method == 'POST' :
        print(request.POST)
        pk=kwargs.get('pk')
        brand_name=request.POST['brand_name']
        brand_description=request.POST['description']
        category=request.POST.getlist('brand_category')
        brand_instence=get_object_or_404(BrandModel, pk=pk)
        brand_instence.title=brand_name
        if len(request.FILES)!=0:
            brand_image=request.FILES['image_brand']
            brand_instence.brand_images=brand_image
        brand_instence.discription=brand_description
        brand_instence.modified_id=request.user
        brand_instence.modified_ip=get_client_ip(request)
        brand_instence.record_status='modified'
        brand_instence.save()
        brand_instence.brand_category.clear()
        for i in category:
            brand_instence.brand_category.add(i)
        return redirect('category:brand')
    
@staff_member_required(login_url='accounts:maxmin_admin')
def delete_brand_category(request,*args,**kwargs):
    brand_category_pk = request.POST.get('id', None)
    brand_instence_pk = request.POST.get('pk', None)
    brand_instence=get_object_or_404(BrandModel, pk=brand_instence_pk)
    brand_instence.modified_id=request.user
    brand_instence.modified_ip=get_client_ip(request)
    brand_instence.record_status='modified'
    brand_instence.brand_category.remove(brand_category_pk)
    brand_instence.save()
    return JsonResponse({'data':True})

@staff_member_required(login_url='accounts:maxmin_admin')
def delete_brand(request,*args,**kwargs):
    brand_instence_pk = request.POST.get('pk', None)
    brand_instence=get_object_or_404(BrandModel, pk=brand_instence_pk)
    brand_instence.modified_id=request.user
    brand_instence.modified_ip=get_client_ip(request)
    brand_instence.record_status='deleted'
    brand_instence.is_active=False
    brand_instence.save()
    brand_instence.brand_category.clear()
    return JsonResponse({'data':True})

@staff_member_required(login_url='accounts:maxmin_admin')
def brand_is_active(request,*args,**kwargs):
    brand_instence_pk = request.POST.get('pk', None)
    brand_instence=get_object_or_404(BrandModel, pk=brand_instence_pk)
    brand_instence.modified_id=request.user
    brand_instence.modified_ip=get_client_ip(request)
    brand_instence.record_status='modified'
    if brand_instence.is_active ==  True:
        brand_instence.is_active = False
        status=False
    else:
        brand_instence.is_active = True
        status=True
    brand_instence.save()
    return JsonResponse({'data':status})
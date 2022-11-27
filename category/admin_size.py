from django.shortcuts import get_object_or_404,redirect
from django.views.generic import ListView,View
from .models import Category as CategoryModels,Size as SizeModel
from cart.order import get_client_ip
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

def size_list(request, *args, **kwargs):
    lists = CategoryModels.objects.filter(level = 0).exclude(record_status = 'deleted')
    size={}
    for i in lists:
        size_list=SizeModel.objects.filter(category=i).exclude(record_status='deleted')
        size.update({i:size_list})
    return size


@method_decorator(staff_member_required(login_url='accounts:maxmin_admin'),name='dispatch')
class Size(ListView):
    model=SizeModel
    template_name = 'admin_/categories/size/size.html'
    context_object_name = 'size_category'
    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['size'] = size_list(self)
        return context   
    
@staff_member_required(login_url='accounts:maxmin_admin')
def add_size(request, **kwargs):
    try:
        category_id = request.POST.get('category', None)
        parent_category=get_object_or_404(CategoryModels,pk=category_id)
        size = request.POST.get('text', None)
        description = request.POST.get('description', None)
       
        size_instence=SizeModel()
        size_instence.category=parent_category
        size_instence.Size=size    
        size_instence.discription=description
        size_instence.created_id=request.user
        size_instence.created_ip=get_client_ip(request)
        size_instence.save()
        template=render_to_string('admin_/categories/size/response-size.html',{'size':size_list(request)})
        return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False}) 

@staff_member_required(login_url='accounts:maxmin_admin')
def edit_size(request,*args,**kwargs):
    try:
        pk = request.POST.get('id', None)
        size_instence=get_object_or_404(SizeModel,pk=pk)
        category_id = request.POST.get('category', None)
        parent_category=get_object_or_404(CategoryModels,pk=category_id)
        size = request.POST.get('text', None)
        description = request.POST.get('description', None)
                 
        size_instence.category=parent_category
        size_instence.Size=size  
        size_instence.discription=description
        size_instence.modified_id=request.user
        size_instence.modified_ip=get_client_ip(request)
        size_instence.record_status='modified'
        size_instence.save()
        template=render_to_string('admin_/categories/size/response-size.html',{'size':size_list(request)})
        return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False})    
    
@staff_member_required(login_url='accounts:maxmin_admin')  
def delete_size(request,*args,**kwargs):
    size_id = request.POST.get('id', None)
    size_instence=get_object_or_404(SizeModel,pk=size_id)
    size_instence.is_active=False
    size_instence.record_status='deleted'
    size_instence.modified_id=request.user
    size_instence.modified_ip=get_client_ip(request)
    size_instence.save()
    template=render_to_string('admin_/categories/size/response-size.html',{'size':size_list(request)})
    return JsonResponse({'data':True,'template':template})

@staff_member_required(login_url='accounts:maxmin_admin')  
def size_is_active(request,*args,**kwargs):
    size_id = request.POST.get('id', None)
    size_instence=get_object_or_404(SizeModel,pk=size_id)
    if size_instence.is_active ==  True:
        size_instence.is_active = False
        status=False
    else:
        size_instence.is_active = True
        status=True
    size_instence.modified_id=request.user
    size_instence.modified_ip=get_client_ip(request)
    size_instence.record_status='modified'
    size_instence.save()
    return JsonResponse({'data':status})
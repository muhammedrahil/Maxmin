from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .forms import *
from .models import Category as CategoryModel
from cart.order import get_client_ip
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


def category_list(request,*args,**kwargs):
    lists= CategoryModel.objects.filter(level=0).exclude(record_status='deleted')
    category={}
    for i in lists:
        category_list=CategoryModel.objects.filter(tree_id=i.tree_id).exclude(id=i.pk).exclude(record_status='deleted')
        category.update({i:category_list})
    return category



@method_decorator(staff_member_required(login_url='accounts:maxmin_admin'),name='dispatch')
class Category(ListView):
    model=Category
    template_name = 'admin_/categories/category/category.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories'] = category_list(self)
        context['category']=CategoryModel.objects.filter(level=0).exclude(record_status='deleted',is_active=False)
        return context   


@staff_member_required(login_url='accounts:maxmin_admin')
def add_category(request, **kwargs):
    try:
        if request.method == 'POST':
            category_id = request.POST.get('category', None)
            category = request.POST.get('text', None)
            description = request.POST.get('description', None)
            if len(category_id) == 0:
                parent_category= None
                if CategoryModel.objects.filter(category__iexact=category,is_active=True,level=0).exists():
                    return JsonResponse({'data':False,'massages':True})  
            else: 
                parent_category=get_object_or_404(CategoryModel,pk=category_id)
                if CategoryModel.objects.filter(category__iexact=category,is_active=True,parent=parent_category).exists():
                    return JsonResponse({'data':False,'massages':True}) 
         
            category_instence=CategoryModel()
            category_instence.category=category
            category_instence.parent=parent_category    
            category_instence.description=description
            category_instence.created_id=request.user
            category_instence.created_ip=get_client_ip(request)
            category_instence.save()
            template=render_to_string('admin_/categories/category/response-category.html',{'categories':category_list(request)})
            return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False})
    
@staff_member_required(login_url='accounts:maxmin_admin')    
def edit_category(request, **kwargs):
    try:
        pk = request.POST.get('id', None)
        category_instence=get_object_or_404(CategoryModel,pk=pk)
        category_id = request.POST.get('category', None)
        if len(category_id) == 0:
            parent_category= None
        else: 
            parent_category=get_object_or_404(CategoryModel,pk=category_id)
        category = request.POST.get('text', None)
        description = request.POST.get('description', None)
        if category_instence.category != category:
            if CategoryModel.objects.filter(category=category).exists():
                return JsonResponse({'data':False,'massages':True})           
        category_instence.category=category
        category_instence.parent=parent_category    
        category_instence.description=description
        category_instence.modified_id=request.user
        category_instence.modified_ip=get_client_ip(request)
        category_instence.record_status='modified'
        category_instence.save()
        template=render_to_string('admin_/categories/category/response-category.html',{'categories':category_list(request)})
        return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False})    

@staff_member_required(login_url='accounts:maxmin_admin')   
def delete_category(request, **kwargs):
    category_id = request.POST.get('id', None)
    parent_category=get_object_or_404(CategoryModel,pk=category_id)
    parent_category.is_active=False
    parent_category.record_status='deleted'
    parent_category.modified_id=request.user
    parent_category.modified_ip=get_client_ip(request)
    parent_category.save()
    try:
        parent_category_subCategory=CategoryModel.objects.filter(parent=parent_category)
        if len(parent_category_subCategory)>0:
            for i in parent_category_subCategory:
                i.is_active=False
                i.modified_id=request.user
                i.modified_ip=get_client_ip(request)
                i.record_status='deleted'
                i.save()
    except:
        pass
    template=render_to_string('admin_/categories/category/response-category.html',{'categories':category_list(request)})
    return JsonResponse({'data':True,'template':template})

@staff_member_required(login_url='accounts:maxmin_admin')
def category_active(request,*args,**kwargs):
    category_id = request.POST.get('id', None)
    parent_category=get_object_or_404(CategoryModel,pk=category_id)
    if parent_category.is_active == True:      
        parent_category.is_active=False
        try:
            parent_category_subCategory=CategoryModel.objects.filter(parent=parent_category)
            if len(parent_category_subCategory)>0:
                for i in parent_category_subCategory:
                    i.is_active=False
                    i.save()
        except:
            pass
        status=False
    else:
        parent_category.is_active=True
        try:
            parent_category_subCategory=CategoryModel.objects.filter(parent=parent_category)
            if len(parent_category_subCategory)>0:
                for i in parent_category_subCategory:
                    i.is_active=True
                    i.save()
        except:
            pass
        status=True
    parent_category.modified_id=request.user
    parent_category.modified_ip=get_client_ip(request)
    parent_category.record_status='modified'
    parent_category.save()
    template=render_to_string('admin_/categories/category/response-category.html',{'categories':category_list(request)})
    return JsonResponse({'data':status,'template':template})
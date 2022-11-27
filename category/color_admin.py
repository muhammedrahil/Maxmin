from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import  Color as ColorAdmin
from cart.order import get_client_ip
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


@method_decorator(staff_member_required(login_url='accounts:maxmin_admin'),name='dispatch')
class Color(ListView):
    model=ColorAdmin
    template_name = 'admin_/categories/color/color.html'
    context_object_name = 'color'
    
    def get_queryset(self) :
        return self.model.objects.exclude(record_status='deleted')
    

@staff_member_required(login_url='accounts:maxmin_admin')
def add_color(request, **kwargs):
    try:
        color_code = request.POST.get('color_code', None)
        color_name = request.POST.get('color_name', None)
        color_description = request.POST.get('color_description', None)
        print(color_description,color_name,color_code)
        color_instence=ColorAdmin()
        color_instence.title=color_name
        color_instence.color_code=color_code    
        color_instence.discription=color_description
        color_instence.created_id=request.user
        color_instence.created_ip=get_client_ip(request)
        color_instence.save()
        template=render_to_string('admin_/categories/color/responce-color.html',{'color':ColorAdmin.objects.exclude(record_status='deleted')})
        return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False}) 
    
@staff_member_required(login_url='accounts:maxmin_admin')   
def edit_color(request,*args,**kwargs):
    try:
        pk = request.POST.get('id', None)
        color_instence=get_object_or_404(ColorAdmin,pk=pk)
        color_code = request.POST.get('color_code', None)
        color_name = request.POST.get('color_name', None)
        color_description = request.POST.get('color_description', None)
        color_instence.title=color_name
        color_instence.color_code=color_code  
        color_instence.discription=color_description
        color_instence.modified_id=request.user
        color_instence.modified_ip=get_client_ip(request)
        color_instence.record_status='modified'
        color_instence.save()
        template=render_to_string('admin_/categories/color/responce-color.html',{'color':ColorAdmin.objects.exclude(record_status='deleted')})
        return JsonResponse({'data':True,'template':template})
    except:
        return JsonResponse({'data':False})    
    
    
@staff_member_required(login_url='accounts:maxmin_admin')  
def delete_color(request,*args,**kwargs):
    try:
        pk = request.POST.get('id', None)
        size_instence=get_object_or_404(ColorAdmin,pk=pk)
        size_instence.modified_id=request.user
        size_instence.modified_ip=get_client_ip(request)
        size_instence.record_status='deleted'
        size_instence.save()
        return JsonResponse({'data':True})
    except:
        return JsonResponse({'data':False})  
   
   
   
@staff_member_required(login_url='accounts:maxmin_admin')
def color_is_active(request,*args,**kwargs):
    pk = request.POST.get('id', None)
    color_instence=get_object_or_404(ColorAdmin,pk=pk)
    if color_instence.is_active ==  True:
        color_instence.is_active = False
        status=False
    else:
        color_instence.is_active = True
        status=True
    color_instence.modified_id=request.user
    color_instence.modified_ip=get_client_ip(request)
    color_instence.record_status='modified'
    color_instence.save()
    return JsonResponse({'data':status})
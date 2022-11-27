from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import VerificationUser,UserAddress,User
import base64
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='accounts:maxmin_admin')
def user_list(request,*args,**kwargs):
  try:
    user_list= VerificationUser.objects.select_related('user').exclude(user__is_superadmin=True)
    context={
      'user_list':user_list,
      'current_site':str(get_current_site(request))
    }
    return render(request,'admin_/users/user.html',context)
  except:
    return render(request,'massages/404.html')


@staff_member_required(login_url='accounts:maxmin_admin')
def admin_user_address(request,*args,**kwargs):
  try:
    pk=kwargs.get('pk')
    user_pk = base64.b64decode(pk)
    pk = user_pk.decode('ascii')
    user=get_object_or_404(User,pk=pk)
    address=UserAddress.objects.filter(user=user)
    print(address)
    context={
      'address':address,
      'user':user
    }
    return render(request,'admin_/users/user-address.html',context)
  except:
    return render(request,'massages/404.html')
  
@staff_member_required(login_url='accounts:maxmin_admin')
def block_user(request,*args,**kwargs):
  pk=request.POST.get('pk')
  user=get_object_or_404(User,pk=pk)
  user.is_active=False
  user.save()
  return JsonResponse({'data':True})  

@staff_member_required(login_url='accounts:maxmin_admin')
def Active_user(request,*args,**kwargs):
  pk=request.POST.get('pk')
  user=get_object_or_404(User,pk=pk)
  user.is_active=True
  user.save()
  return JsonResponse({'data':True})  
from django.shortcuts import render,get_object_or_404,redirect
from .models import Coupon,RedeamCoupen
from django.utils import timezone



def user_coupen(request,*args,**kwargs):
  valid=Coupon.objects.filter(is_active=True,expiry_date__gte=timezone.now())
  redeam=RedeamCoupen.objects.filter(created_id=request.user)
  redeam_id=redeam.values('coupon')
  id=[]
  for i in redeam_id:
    id.append(i['coupon'])
  valid=valid.exclude(pk__in=id)
  expire=Coupon.objects.filter(expiry_date__lte=timezone.now())
  context={
    'valid':valid,
    'redeam':redeam,
    'expire':expire
  }
  return render(request,'user/coupen/coupen.html',context)
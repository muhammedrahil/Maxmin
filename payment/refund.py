from django.shortcuts import render
from .models import RefundPayment
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='accounts:maxmin_admin')
def refund_list(request,*args,**kwargs):
  try:
    refund_list=RefundPayment.objects.all().order_by('-pk')
    context={
      'refund_list':refund_list,
      'current_site':str(get_current_site(request))
    }
    return render(request,'admin_/order/order-payment-refund/refund.html',context)
  except:
    return render(request,'massages/404.html')
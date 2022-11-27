import base64
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

from .models import CashOnDeliveryTextGenarator
from django.http import JsonResponse
# Create your views here.
import random
from cart.models import *
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from django.core import signing
from django.core.paginator import Paginator

CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

@login_required(login_url='accounts:login')
def cash_on_delivery_code_genarator(request,*args,**kwargs):
    code_genarator=CashOnDeliveryTextGenarator.objects.all()
    list_code=[]
    for i in code_genarator:
        list_code.append(i.id)
    random_text=random.choice(list_code)
    text_instence=get_object_or_404(CashOnDeliveryTextGenarator,pk=random_text)
    return JsonResponse({'data':True,'text_instence':text_instence.text})

@login_required(login_url='accounts:login')
def cash_on_delivery_order_confrim(request,*args,**kwargs):
    product_order_session_id=kwargs.get('product_order_session_id')
    denc = base64.b64decode(product_order_session_id)
    order_id = denc.decode('ascii')
    try:
        order_instence=get_object_or_404(Order,pk=int(order_id))
        if order_instence:
            orders_id='OD'+str(order_instence.id)
            order_instence.orders_id=str(orders_id)
            order_instence.order_date=timezone.now()
            order_instence.order_status='ordered'
            order_instence.is_active=True
            order_instence.save() 
            
            for i in order_instence.products.all():
                cart_intences = get_object_or_404(Cart,pk=i.id,user=request.user)
                cart_intences.is_active=False
                cart_intences.save()
                
            order_status_instence=OrderStatus()
            order_status_instence.order=order_instence
            order_status_instence.order_confirmed=True
            order_status_instence.order_confirmed_date=timezone.now()
            order_status_instence.is_active=True
            if order_instence.delivery_address.state == 'Kerala':
                order_status_instence.delivery_execept_date=timezone.now()+timedelta(days=10)
            else:
                order_status_instence.delivery_execept_date=timezone.now()+timedelta(days=20)
            order_status_instence.save()  
            
            payment_instence=Payment()
            payment_instence.order=order_instence
            payment_instence.order_status=order_status_instence
            payment_instence.user=request.user
            payment_instence.payment_method='Cash On Delivery'
            payment_instence.payment_price=order_instence.totel_payment_price
            payment_instence.payment_status='PENDING'
            payment_instence.is_active=True
            payment_instence.save()



                          
            email=order_instence.order_confirmation_email
            mail_subject = "Order Infermation"
            current_site = get_current_site(request)
            massage = render_to_string('user/payment-order/order-infermation-email.html',
            {
                'order_instence': order_instence,
                'domain'  : current_site,
                'totel': payment_instence.payment_price
            })
            send_email = EmailMessage(mail_subject,massage,to=[email])
            send_email.send()
            
            order_id=signing.dumps(str(order_instence.id))
            payment_id=signing.dumps(str(payment_instence.id))
            order_status_id=signing.dumps(str(order_status_instence.id))
            return redirect('payment:order_placed',order_id=order_id,payment_id=payment_id,order_status_id=order_status_id)
    except:
        return render(request,'user/status/failed.html')

@login_required(login_url='accounts:login')
def order_placed(request,*args,**kwargs):
    try:
        order_id_prm = kwargs.get('order_id')
        payment_id_prm = kwargs.get('payment_id')
        order_status_id_prm = kwargs.get('order_status_id')
        order_id=signing.loads(order_id_prm)
        payment_id=signing.loads(payment_id_prm)
        order_status_id=signing.loads(order_status_id_prm)
        
        try:
            del request.session['order_id']
            del request.session['length_product']  
        except:    
            pass
        
        order_instence=get_object_or_404(Order,pk=order_id)
        payment_instence=get_object_or_404(Payment,pk=payment_id)
        order_status_instence=get_object_or_404(OrderStatus,pk=order_status_id)

        context={
            'order':order_instence,
            'payment':payment_instence,
            'orderstatus':order_status_instence,
            'cancel_reasons': CancelReasons.objects.all(),
            'payment_instence':payment_instence,
            'order_id':signing.dumps(str(order_status_instence.id)),
            'payment_id':signing.dumps(str(payment_instence.id)),
            'refund': RefundPayment.objects.filter(order_status=order_status_instence,order=order_instence,user=request.user,refund_status=True)
            
        }
        return render(request,'user/payment-order/order-placed.html',context)
    except:
        return render(request,'user/status/404.html')
    
@login_required(login_url='accounts:login')
def cancel_order(request,*args,**kwargs):
    refund_exp_time=''
    status=False
    try:
        order_status_id_enc = request.POST.get('order_status_id', None)
        order_status_id=signing.loads(order_status_id_enc)
        payment_status_id_enc = request.POST.get('payment_status_id', None)
        payment_status_id=signing.loads(payment_status_id_enc)
        reasons = request.POST.get('reasons', None)
        comments = request.POST.get('comments', None)
        order_instence=get_object_or_404(OrderStatus,pk=order_status_id)
        order_instence.Cancelled=True
        reasons_instence=get_object_or_404(CancelReasons,pk=reasons)
        order_instence.cancelReasons=reasons_instence
        order_instence.cancel_reason_descrition=comments
        order_instence.cancelled_date=timezone.now()
        order_instence.save()
        payment_instence=get_object_or_404(Payment,pk=payment_status_id)
        if payment_instence.payment_status != 'Pending':
            refund_payment=RefundPayment()
            refund_payment.user=request.user
            refund_payment.order=order_instence.order
            refund_payment.payment=payment_instence
            refund_payment.order_status=order_instence
            refund_payment.refund_status=True
            refund_payment.execept_refund_date=timezone.now()+timedelta(days=8)
            refund_payment.save()
            refund_exp_time=(refund_payment.execept_refund_date).strftime("%m-%d-%Y")
            status=True
        else:
            status=False
            refund_exp_time='your Not payed , so No Refunds'
    except:
        status=False
        refund_exp_time=''
    template=render_to_string('user/payment-order/status.html',{'orderstatus':order_instence})
    return JsonResponse({'status':status,'refund_exp_time':refund_exp_time,'template':template})



@login_required(login_url='accounts:login')
def order_deatails(request,*args,**kwargs):
    try:
        # if cache.get('order_deatails'):
        #     context=cache.get('order_deatails')
        #     print("DATA COMING FROM CASHE")
        # else: 
        print("DATA COMING FROM DB")
        order_inseteses=Payment.objects.select_related('order','order_status').filter(order__user=request.user,order__is_active=True,order_status__is_active=True,is_active=True).order_by('-order__order_date')
        # order_inseteses=OrderStatus.objects.select_related('order').filter(order__user=request.user,order__is_active=True,is_active=True).order_by('-order__order_date')
        paginator = Paginator(order_inseteses, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={
            'order':page_obj
        }
        # cache.set('order_deatails',context)
        return render(request,'user/payment-order/order-deatails/orders.html',context)
    except:
        return render(request,'user/status/404.html')
    
@login_required(login_url='accounts:login')
def search_order(request,*args,**kwargs):
    search_order = request.POST.get('search_order')
    cart_instence=Cart.objects.filter(product__product__product_name__icontains=search_order).distinct()    
    # if cache.get(['order_deatails',cart_instence]):
    #     print("DATA COMING FROM cash")
    #     order_inseteses=cache.get(['order_deatails',cart_instence])
    # else:
    # print("DATA COMING FROM DB")
    order_inseteses=Payment.objects.select_related('order','order_status').filter(order__user=request.user,order__is_active=True,order_status__is_active=True,is_active=True).order_by('-order__order_date')
    order_inseteses=order_inseteses.filter(order__products__in=cart_instence)
    # cache.set(['order_deatails',cart_instence],order_inseteses)        
    template=render_to_string('user/payment-order/order-deatails/order-product.html',{'order':order_inseteses})
    return JsonResponse({'data':True,'template':template})


@login_required(login_url='accounts:login')
def filter_orders(request,*args,**kwargs):
    Confrimed=request.GET.getlist('Confrimed[]')
    Shipped=request.GET.getlist('Shipped[]')
    Out_for_delivery=request.GET.getlist('Out_for_delivery[]')
    Delivered=request.GET.getlist('Delivered[]')
    Cancelled=request.GET.getlist('Cancelled[]')
    Returned=request.GET.getlist('Returned[]')
    order_inseteses=Payment.objects.select_related('order','order_status').filter(order__user=request.user,order__is_active=True,order_status__is_active=True,is_active=True).order_by('-order__order_date')
    
    if len(Confrimed)>0:
        order_inseteses=order_inseteses.filter(order_status__current_status=1)
    if len(Shipped)>0:
        order_inseteses=order_inseteses.filter(order_status__current_status=2)        
    if len(Out_for_delivery)>0:
        order_inseteses=order_inseteses.filter(order_status__current_status=3)
    if len(Delivered)>0:
        order_inseteses=order_inseteses.filter(order_status__current_status=4)       
    if len(Cancelled)>0:
        order_inseteses=order_inseteses.filter(order_status__current_status=5)       
    # if len(Returned)>0:
    #     order_inseteses=order_inseteses.filter(order_confirmed=True)   
    print(order_inseteses,Cancelled)     
    template=render_to_string('user/payment-order/order-deatails/order-product.html',{'order':order_inseteses})
    return JsonResponse({'data':True,'template':template})
    
    
@login_required(login_url='accounts:login')
def order_placed_history(request,*args,**kwargs):
    try:
        orderpk=kwargs.get('orderpk')
        itemid=kwargs.get('itemid')
        statusid=kwargs.get('sid')
        payment_id=kwargs.get('payid')
        
        order_instence=get_object_or_404(Order,pk=orderpk)
        order_status_instence=get_object_or_404(OrderStatus,pk=statusid)  
        cart_instence=get_object_or_404(Cart,pk=itemid)
        payment_instence=get_object_or_404(Payment,pk=payment_id)
        context={
            'order':order_instence,
            'orderstatus':order_status_instence,     
            'cart':cart_instence,
            'payment_instence':payment_instence,
            'cancel_reasons': CancelReasons.objects.all(),
            'order_id':signing.dumps(str(order_status_instence.id)),
            'payment_id':signing.dumps(str(payment_instence.id)),
        }
        return render(request,'user/payment-order/order-placed-history/order-placed-history.html',context)
    except:
        return render(request,'user/status/404.html')
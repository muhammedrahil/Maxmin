
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from cart.models import *
from .models import *
from datetime import timedelta
import base64
from django.utils import timezone
from cart.order import get_client_ip
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def paypal(request,*args,**kwargs):
    oreder_id=request.POST.get('product_order_session_id')
    transaction_id=request.POST.get('transaction_id')
    transaction_status=request.POST.get('transaction_status')
    orderData_id=request.POST.get('orderData_id')
    payer_id=request.POST.get('payer')

    dnc = base64.b64decode(oreder_id)
    oreder_id = dnc.decode('ascii')
    
    order_instence=get_object_or_404(Order,pk=int(oreder_id))
    if order_instence:
        orders_id='OD'+str(order_instence.pk)
        order_instence.orders_id=str(orders_id)
        order_instence.order_date=timezone.now()
        order_instence.order_status='ordered'
        order_instence.is_active=True
        order_instence.save()
        
        for i in order_instence.products.all():
            cart_intences = get_object_or_404(Cart,pk=i.id,user=order_instence.user)
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
        payment_instence.user=order_instence.user
        payment_instence.order_status=order_status_instence
        payment_instence.payment_method='PAYPAL'
        payment_instence.payment_order_id=orderData_id
        payment_instence.payment_id=transaction_id
        payment_instence.payer_id=payer_id
        payment_instence.payment_date=timezone.now()
        payment_instence.ip=get_client_ip(request)
        payment_instence.payment_price=order_instence.totel_payment_price
        payment_instence.payment_status=transaction_status
        payment_instence.payment_complete_status=True
        payment_instence.is_active=True
        payment_instence.save()
        try:
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
        except:
            pass
        order_id=signing.dumps(str(order_instence.pk))
        payment_id=signing.dumps(str(payment_instence.pk))
        order_status_id=signing.dumps(str(order_status_instence.pk))
        return JsonResponse({'data':True,'order_id':order_id,'payment_id':payment_id,'order_status_id':order_status_id})

from django.shortcuts import render,get_object_or_404,redirect
from accounts.models import User,UserAddress
from .models import Cart, Order
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from accounts.forms import UserAddressForm
from django.conf import settings
import razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
from django.contrib.sites.shortcuts import get_current_site

import base64


@login_required(login_url='accounts:login')
def checkout(request,*args,**kwargs):    
    
    
    # if  'order_id' in request.session:
    #     del request.session['order_id']
    # try:
        user_infermations=request.user
        cart_products=Cart.objects.filter(user=user_infermations,is_active=True)
        user_address_form=UserAddressForm()
        if len(cart_products) != 0:
            user_address=UserAddress.objects.filter(user=user_infermations)
            data=cart_products.aggregate(Sum('totel_qty_price'),Sum('product_qty'),Sum('totel_unit_price'))
            length_product=data['product_qty__sum']

            try:
                totel_price=float(data['totel_qty_price__sum'])
                Totel_unit_price=float(data['totel_unit_price__sum'])
            except:
                totel_price=00.0
                Totel_unit_price=00.0

            savings=float(Totel_unit_price)-totel_price
            callback_url = str(get_current_site(request))

            context={
            'login':user_infermations,
            'user_address':user_address,
            'checkout_product': cart_products,
            'length_product':length_product,
            'totel_price':totel_price,
            'savings':savings,
            'Totel_unit_price':Totel_unit_price,
            'RAZORPAY_KEY_ID':settings.RAZORPAY_KEY_ID,
            'callback_url':callback_url,
            'user_address_form':user_address_form
            }

            try:
                if 'order_id' in request.session:
                    order_instence=get_object_or_404(Order,pk=request.session['order_id'])
                    context['totel_price']=order_instence.totel_payment_price
                    context.update({'order':order_instence})
                    data = {
                    "amount": float(order_instence.totel_payment_price*100),
                    "currency": "INR",
                    "receipt": order_instence.orders_id,
                    "payment_capture": "1"      
                    }
                    context.update({'user_checkout_address':order_instence.delivery_address.name})
                    order_id = client.order.create(data)
                    context.update({'order_id':order_id['id']})
                    product_order_id=str(order_instence.id)
                    enc = base64.b64encode(product_order_id.encode('ascii'))
                    enc=enc.decode()
                    context.update({'product_order_id':enc})
                    print('SESSION IN')
            except:
                pass
            return render(request,'user/checkout/checkout.html',context)
        else:
            return redirect('cart:cart')
    # except:
    #     return render(request,'user/status/404.html')
    

@login_required(login_url='accounts:login')
def delivery_address(request,*args,**kwargs):
    address_id = request.POST.get('id', None)
    checkout_address=get_object_or_404(UserAddress,pk=address_id)
    template =render_to_string('user/checkout/checkout-delivery-address.html',{'delivery_address':checkout_address})
    return JsonResponse({'data':template}) 



@login_required(login_url='accounts:login')
def delete_checkout_items(request,*args,**kwrgs):
    try:
        cart_id = request.POST.get('cart_id', None)
        if request.user.is_authenticated:
            instence=get_object_or_404(Cart,pk=cart_id)
            instence.deleted_date=timezone.now()
            instence.is_active=False
            instence.save()
            cart_products=Cart.objects.filter(user=request.user,is_active=True)
            data=cart_products.aggregate(Sum('totel_qty_price'),Sum('product_qty'),Sum('totel_unit_price'))
            length_product=data['product_qty__sum']
            totel_price=float(data['totel_qty_price__sum'])
            Totel_unit_price=float(data['totel_unit_price__sum'])
            savings=float(Totel_unit_price)-totel_price
            status=True
    except:
        status=False
        totel_price=0
        length_product=0
        savings=0
    request.session['length_product']=length_product
    return JsonResponse({'data':status,'length_product':length_product,'totel_price':totel_price,'savings':savings,'Totel_unit_price':Totel_unit_price})



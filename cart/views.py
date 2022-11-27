from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from category.context_processors import category
# Create your views here.
from product.models import *
from .models import Cart
from django.template.loader import render_to_string
from django.db.models import Sum

# single product qty 

def quantity(request,*args,**kwargs):
    prod_id = request.POST.get('prod_id', None)
    product_qwantity  = ProductQuantity.objects.get(pk=prod_id)
    stock=product_qwantity.stock
    nums = range(1,stock+1)
    stock=list(nums)
    template =render_to_string('user/single-product-section/quanity.html',{'data':stock})
    return JsonResponse({'data':template}) 



def add_to_cart(request,*args,**kwargs):
    id = request.POST.get('size', None)
    quantity = request.POST.get('qty', None) 
    product_quantity = ProductQuantity.objects.get(pk=id)
    offerprice=product_quantity.product.offerprice
    if request.user.is_authenticated:
        cart=Cart.objects.filter(is_active=True,user=request.user)
        in_cart_product=Cart.objects.filter(product_quantity=product_quantity,is_active=True,user=request.user)
        if len(cart) != 0 and len(in_cart_product) != 0 :
            in_cart_product=in_cart_product[0]
            in_cart_product.user=request.user
            in_cart_product.product_quantity=product_quantity
            in_cart_product.product=product_quantity.product
            in_cart_product.product_qty=int(quantity)
            in_cart_product.unit_price=product_quantity.product.product.unit_price
            in_cart_product.product_price=offerprice
            in_cart_product.totel_qty_price=offerprice*int(quantity)
            in_cart_product.save()
        else:
            cart=Cart()
            cart.user=request.user
            cart.product_quantity=product_quantity
            cart.product=product_quantity.product
            cart.product_qty=int(quantity)
            cart.unit_price=product_quantity.product.product.unit_price
            cart.product_price=offerprice
            cart.totel_qty_price=offerprice*int(quantity)
            cart.save()
        data=Cart.objects.filter(user=request.user,is_active=True).aggregate(Sum('totel_qty_price'),Sum('product_qty'))
        responce_data={}
        responce_data['product_qty']=data['product_qty__sum']
        length_product=data['product_qty__sum'] 
        responce_data['price']=float(data['totel_qty_price__sum'])
    else:          
        cart={}
        cart[str(product_quantity.id)]={
            'price': float(offerprice),
            'product_qty': int(quantity)
        }
        if 'cartdata' in request.session:
            if str(product_quantity.id) in request.session['cartdata']:
                cart_d=request.session['cartdata']
                cart_d[str(product_quantity.id)]['product_qty'] = int(cart[str(product_quantity.id)]['product_qty'])
                cart_d.update(cart_d)
                request.session['cartdata']=cart_d
            else:
                cart_d=request.session['cartdata']
                cart_d.update(cart)
                cart_d.update(cart_d)
                request.session['cartdata']=cart_d
        else:
            request.session['cartdata']=cart                  
        length_product=0
        price=0
        for key in request.session['cartdata']:
            length_product += int(request.session['cartdata'][key]['product_qty'])
            count_qty=int(request.session['cartdata'][key]['product_qty'])
            price += float(request.session['cartdata'][key]['price'])*count_qty
            sub_totel_price = float(request.session['cartdata'][key]['price'])*count_qty
            request.session['cartdata'][key].update({'sub_totel_price':sub_totel_price})
            cart_product=ProductQuantity.objects.get(pk=key)
            request.session['cartdata'][key].update({'cart_product':cart_product.product.product.product_name})
            request.session['cartdata'][key].update({'image':cart_product.product.images.url})
        responce_data={'product_qty':length_product,'price':price}
    category(request)
    request.session['length_product']=length_product 
    template =render_to_string('user/single-product-section/responce-data.html',{'data':responce_data})
    return JsonResponse({'data':template,'totel_count_cart': length_product}) 


def cart(request,*args,**kwargs):
    try:
        if request.user.is_authenticated:                
            cart_products=Cart.objects.filter(user=request.user).filter(is_active=True)  
            cart_data={}
            
            if len(cart_products) != 0:
                for i in cart_products:
                    cart_product=ProductQuantity.objects.get(pk=i.product_quantity.id)
                    stock=cart_product.stock
                    nums = range(1,stock+1)
                    stock=list(nums)
                    cart_data[str(i.id)]={
                        'prod':i,
                        'product_size':ProductQuantity.objects.filter(product=i.product),
                        'stock':stock,
                    }
                data=cart_products.aggregate(Sum('totel_qty_price'),Sum('product_qty'),Sum('totel_unit_price'))
                length_product=data['product_qty__sum']
                totel_price=float(data['totel_qty_price__sum'])
                Totel_unit_price=float(data['totel_unit_price__sum'])  
                savings=float(Totel_unit_price)-totel_price
                request.session['length_product']=length_product
                status=True
            else:
                status=False
                cart_data=False
                totel_price=00
                savings=00
                length_product=00
        else:
            if 'cartdata' in request.session:
                totel_price=0
                length_product=0
                Totel_unit_price=0
                cart_data=request.session['cartdata']
                for key in list(cart_data):
                    length_product += int(cart_data[key]['product_qty'])
                    count_qty =int(cart_data[key]['product_qty'])
                    cart_product=ProductQuantity.objects.get(pk=key)
                    cart_data[key].update({'unit_price':float(cart_product.product.product.unit_price)})
                    cart_data[key].update({'cart_product':cart_product.product.product.product_name})
                    cart_data[key].update({'image':cart_product.product.images2.url})
                    totel_price += float(cart_data[key]['price'])*count_qty
                    Totel_unit_price += float(cart_product.product.product.unit_price)*count_qty
                    prod_id=cart_product.product.id
                    product_qwantity  = ProductQuantity.objects.filter(product=prod_id)
                    product_size={}
                    for i in product_qwantity:
                        product_size[str(i.id)]={
                            'product_size':i.product_size.Size,
                        } 
                    cart_data[key].update({'prod_size':product_size})
                    stock=cart_product.stock
                    nums = range(1,stock+1)
                    stock=list(nums)
                    cart_data[key].update({'stock':stock})
                savings = Totel_unit_price-totel_price
                request.session['length_product']=length_product
                request.session['cartdata']=cart_data
                if len(request.session['cartdata']) == 0:
                    status=False
                else:
                    status=True
            else:
                status=False
                cart_data=False
                totel_price=00
                savings=00
                length_product=00
            
        return render(request,'user/cart/cart-section.html',{ 
                    'data':cart_data,'totel_price':totel_price,'status':status,'length_product':length_product,'savings':savings})
    except:
        return render(request,'user/status/404.html')
        
    

def price_change(request,*args,**kwargs):
    qty = request.POST.get('qty', None)
    key = request.POST.get('key', None)
    if request.user.is_authenticated:
        cart_data=Cart.objects.get(pk=key)
        cart_data.product_qty=int(qty)
        cart_data.totel_qty_price=cart_data.product_price*int(qty)
        cart_data.save()
        sub_totel_price=cart_data.totel_qty_price
        cart_products=Cart.objects.filter(user=request.user,is_active=True)
        data=cart_products.aggregate(Sum('totel_qty_price'),Sum('product_qty'),Sum('totel_unit_price'))
        length_product=data['product_qty__sum']
        totel_price=float(data['totel_qty_price__sum'])
        Totel_unit_price=float(data['totel_unit_price__sum'])
        savings=float(Totel_unit_price)-totel_price
    else:
        cart_data=request.session['cartdata']
        price= float(cart_data[key]['price'])*int(qty)
        cart_data[key].update({'sub_totel_price':price,'product_qty':int(qty)})
        cart_data.update(cart_data)
        sub_totel_price=cart_data[key]['sub_totel_price']
        request.session['cartdata']=cart_data
        length_product=0
        totel_price=0
        Totel_unit_price=0
        for key in request.session['cartdata']:
            length_product += int(request.session['cartdata'][key]['product_qty'])
            count_qty=int(request.session['cartdata'][key]['product_qty'])
            totel_price += float(request.session['cartdata'][key]['price'])*count_qty
            Totel_unit_price += float(request.session['cartdata'][key]['unit_price'])*count_qty
        savings = Totel_unit_price-totel_price
    request.session['length_product']=length_product
    return JsonResponse({
        'data':sub_totel_price,'totel_count_cart':length_product,'totel_price':totel_price,'savings':savings})



def deleted_cart_items(request,*args,**kwargs):
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
        else:
            cart_data=request.session['cartdata']
            del cart_data[cart_id]
            length_product=0
            totel_price=0
            Totel_unit_price=0
            for key in cart_data:
                length_product += int(cart_data[key]['product_qty'])
                count_qty=int(cart_data[key]['product_qty'])
                totel_price += float(cart_data[key]['price'])*count_qty
                Totel_unit_price += float(cart_data[key]['unit_price'])*count_qty
            savings = Totel_unit_price-totel_price
            request.session['cartdata']=cart_data
            if len(request.session['cartdata']) == 0:
                status=False
            else:
                status=True
    except:
        status=False
        totel_price=0
        length_product=0
        savings=0
    request.session['length_product']=length_product
    return JsonResponse({'data':status,'length_product':length_product,'totel_price':totel_price,'savings':savings})

# jest comment

def size_change(request,*args,**kwargs):
    session_id = request.POST.get('id', None)
    size_id = request.POST.get('size', None)
    cart_product=ProductQuantity.objects.get(pk=size_id)
    stock=cart_product.stock
    nums = range(1,stock+1)
    stock=list(nums)
    # if request.user.is_authenticated:
    # print(request.session['cartdata'])
    cart_data=request.session['cartdata']
    print(cart_data[session_id]['prod_size'])
    cart_data[session_id]['stock']=stock
    cart_data[session_id].update({'stock':stock})
    request.session['cartdata']=cart_data
    template =render_to_string('user/cart/quanity.html',{'data':stock,'key':session_id})
    return JsonResponse({'data':template})

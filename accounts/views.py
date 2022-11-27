from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import ReistrationForm,LoginForm,ResetPasswod
from .models import User
from .verify_otp import send_otp,admin_send_otp,verify_otp
# Create your views here.

# email send django library functions
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.db.models import Sum
from cart.models import Cart
from product.models import ProductQuantity
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
import requests
import re
import phonenumbers

def check_mail(request):
    return render(request,'user/accounts/email-check.html')

def user_registration(request,*args,**kwrgs):
    try:
        if request.method == 'POST':
            choice = request.POST['option']
            form = ReistrationForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                phone_no=form.cleaned_data['phone_no']
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                password=form.cleaned_data['password']
                user=User.objects.create_user(email=email,phone_no=phone_no,first_name=first_name,last_name=last_name,password=password)
                user.save()
                if choice == 'email':
                    current_site = get_current_site(request)
                    mail_subject = "Please active your account"
                    massage = render_to_string('user/accounts/verification-email.html',
                        {
                        'user':user,
                        'domain'  : current_site,
                        # user pk encode 
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        # user token genarete
                        'token': default_token_generator.make_token(user),
                    })
                    to_email=email
                    send_email = EmailMessage(mail_subject,massage,to=[to_email])
                    send_email.send()
                    return redirect('accounts:check_mail')
                else:
                    verification_user=send_otp(phone_no,user)
                    return redirect('accounts:otp_verify_code',phone_no=phone_no,uid=user.pk,verification_user=verification_user)
            else:
                messages.warning(request,'Form not submition try again...')
                return redirect('accounts:registration')
                    
        form = ReistrationForm()
        return render(request,'user/accounts/registration.html',{'form':form})
    except:
        return render(request,'user/status/404.html')



def user_login(request,*args,**kwrgs):
    try:
        if request.user.is_authenticated:
            return redirect('landing:landing_page')
        if request.method == 'POST':
            form= LoginForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                user = authenticate(email=email,password=password)
                if user is not None:
                    login(request,user)
                    if 'cartdata' in request.session:
                        session_data=request.session['cartdata']
                        cart=Cart.objects.filter(is_active=True,user=request.user)    
                        if len(cart) !=0:    
                            for key,val in session_data.items():
                                in_cart_product=Cart.objects.filter(product_quantity=key,is_active=True,user=request.user)
                                if   len(in_cart_product) != 0 :
                                    in_cart_product=in_cart_product[0]
                                    in_cart_product.user=request.user
                                    in_cart_product.product_qty+=int(session_data[key]['product_qty'])
                                    in_cart_product.totel_qty_price=in_cart_product.product_price*in_cart_product.product_qty
                                    in_cart_product.save()
                                else:    
                                    cart=Cart()
                                    cart.user=request.user
                                    product_quantity = ProductQuantity.objects.get(pk=int(key))
                                    cart.product_quantity=product_quantity
                                    cart.product=product_quantity.product
                                    cart.session_id=request.session.session_key
                                    cart.unit_price=product_quantity.product.product.unit_price
                                    cart.product_qty=val['product_qty']
                                    cart.product_price=val['price']
                                    cart.totel_qty_price=val['sub_totel_price']
                                    cart.save()
                        else:    
                            for key,val in session_data.items():        
                                cart=Cart()
                                cart.user=request.user
                                product_quantity = ProductQuantity.objects.get(pk=int(key))
                                cart.product_quantity=product_quantity
                                cart.product=product_quantity.product
                                cart.session_id=request.session.session_key
                                cart.unit_price=product_quantity.product.product.unit_price
                                cart.product_qty=val['product_qty']
                                cart.product_price=val['price']
                                cart.totel_qty_price=val['sub_totel_price']
                                cart.save()
                        del request.session['cartdata']
                    
                    data=Cart.objects.filter(user=request.user,is_active=True).aggregate(Sum('product_qty'))
                    length_product=data['product_qty__sum']
                    request.session['length_product']=length_product
                    
                    # redirect paths location 
                    url =request.META.get('HTTP_REFERER')
                    # http://127.0.0.1:8000/accounts/login 
                    try:
                        query = requests.utils.urlparse(url).query
                        # next=/accounts/
                        print(query,'**********************************')
                        params=dict(x.split('=') for x in query.split('&'))
                        # {'next': '/accounts/'}
                        print(params,'**********************************')
                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)        
                    except:
                        return redirect('landing:landing_page')
                else :
                    messages.warning(request,'Incorrect Username or Password')
                    return redirect('accounts:login') 
        form= LoginForm()
        return render(request,'user/accounts/login.html',{'form':form})
    except:
        return render(request,'user/status/404.html')

@never_cache
def maxmin_admin(request,*args,**kwrgs):
    # if request.user.is_authenticated:
    #     if request.user.is_superadmin and request.user.is_staff:
    #         return redirect('landing:dashboard')
    if request.method == 'POST':
        username=request.POST.get('username',None)
        email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        otpnumber=0
        if username.isnumeric():
            try:
                my_number = phonenumbers.parse("+91"+username, "GB")
                if phonenumbers.is_valid_number(my_number):
                    otpnumber=username 
                    user=get_object_or_404(User,phone_no=username,is_staff=True,is_superadmin=True,is_active=True)  
                else:
                    messages.warning(request,'Phone Number not Valid')
                    return redirect('accounts:maxmin_admin')
            except:
                messages.warning(request,'Your a not a admin')
                return redirect('accounts:maxmin_admin')               
        else:
            try:
                if re.fullmatch(email, username):          
                    user=get_object_or_404(User,email=username,is_staff=True,is_superadmin=True,is_active=True)
                    otpnumber=user.phone_no
                else:
                    messages.warning(request,'Email Not Valid')
                    return redirect('accounts:maxmin_admin') 
            except:
                messages.warning(request,'Your a not admin')
                return redirect('accounts:maxmin_admin')
        verify_user=admin_send_otp(otpnumber)
        return redirect('accounts:maxmin_admin_otp',phone_no=otpnumber,uid=user.id)
    return render(request,'admin_/auth_/login.html')

@never_cache
def maxmin_admin_otp(request,*args,**kwrgs):
    phone_no=kwrgs.get('phone_no')
    uid=kwrgs.get('uid')
    if request.method == 'POST':
        otp = request.POST['otp']
        verify=verify_otp(phone_no,otp)
        if  verify :
            user=get_object_or_404(User,pk=uid)
            login(request,user)
            return redirect('landing:dashboard')
        else:
            messages.error(request,'invalid otp recheck')
            return redirect('accounts:maxmin_admin_otp')
    return  render(request,'admin_/auth_/otp.html')

@staff_member_required(login_url='accounts:maxmin_admin')   
def admin_logout(request,*args,**kwrgs):
    logout(request)
    return redirect('accounts:maxmin_admin') 


@login_required(login_url='accounts:login')
def user_logout(request,*args,**kwrgs):
    logout(request)
    return redirect('accounts:login') 



def forget_password(request,*args,**kwrgs):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                user =User.objects.get(email__exact=email)
                current_site = get_current_site(request)
                mail_subject = "Reset Your Password"
                massage = render_to_string('user/accounts/reset-password-email.html',
                    {
                    'user':user,
                    'domain'  : current_site,
                    # user pk encode 
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # user token genarete
                    'token': default_token_generator.make_token(user),
                })
                to_email=email
                send_email = EmailMessage(mail_subject,massage,to=[to_email])
                send_email.send()
                return redirect('accounts:check_mail')
            else:
                messages.warning(request,'Email Not Exists , try another email')
                return redirect('accounts:forget_password')         
        return render(request,'user/accounts/forget-password.html')
    except:
        return render(request,'user/status/404.html')

def Reset_password(request,uid):
    try:
        if request.method == 'POST':
            form=ResetPasswod(request.POST)
            if form.is_valid():
                password=form.cleaned_data['password']
                user=User.objects.get(pk=uid)
                user.set_password(password)
                user.save()
        form=ResetPasswod()
        return render(request,'user/accounts/reset-password.html',{'form':form})
    except:
        return render(request,'user/status/404.html')
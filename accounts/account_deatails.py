from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import User,UserAddress
from .forms import UserAddressForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from cart.order import get_client_ip


@login_required(login_url='accounts:login')
def accounts(request,*args,**kwrgs):
    try:
        user_infermations=request.user
        user_address_form=UserAddressForm()
        context={
            'user_infermations':user_infermations,
            'user_address_form':user_address_form,
            'user_address':UserAddress.objects.filter(user=user_infermations,now_is_active=True)
        }
        return render(request,'user/account-deatails/account-deatails.html',context)
    except:
        return render(request,'user/status/404.html')


@login_required(login_url='accounts:login')
def user_address_deatails(request,*args,**kwrgs):
    name = request.POST.get('name', None)
    phone_no = request.POST.get('phone_no', None) 
    pincode = request.POST.get('pincode', None) 
    locality = request.POST.get('locality', None)
    address = request.POST.get('address', None)
    city_district_town = request.POST.get('city_district_town', None) 
    state = request.POST.get('state', None) 
    landmark = request.POST.get('landmark', None)
    alt_phone_no = request.POST.get('alt_phone_no', None) 
    address_type = request.POST.get('addresstype', None) 
    useraddress=UserAddress()
    useraddress.user=request.user
    useraddress.name=name
    useraddress.phone_no=phone_no
    useraddress.pincode=pincode
    useraddress.locality=locality
    useraddress.address=address
    useraddress.city_district_town=city_district_town
    useraddress.state=state
    if len(landmark)>0:
        useraddress.landmark=landmark
    if len(alt_phone_no)>0:
        useraddress.alt_phone_no=alt_phone_no
    useraddress.address_type=address_type
    useraddress.created_id=request.user
    useraddress.created_ip=get_client_ip(request)
    useraddress.save()
    status=True
    return JsonResponse({'data':status})

@login_required(login_url='accounts:login')
def user_infermations(request,*args,**kwrgs):
    try:
        user_id = request.POST.get('user_id', None)
        gender = request.POST.get('gender', None)
        first_name = request.POST.get('first_name', None) 
        last_name = request.POST.get('last_name', None) 
        user=get_object_or_404(User,pk=user_id)
        if len(gender)>0:
            user.gender=gender
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        status=True
    except:
        status=False
    return JsonResponse({'data':status})




@login_required(login_url='accounts:login')
def delete_address(request,*args,**kwrgs):
    try:
        address_id = request.POST.get('address_id', None)
        instence=UserAddress.objects.get(pk=address_id)
        instence.now_is_active=False
        instence.modified_id=request.user
        instence.modified_ip=get_client_ip(request)
        instence.record_status='modified'
        instence.save()
        status=True
    except:
        status=False
    return JsonResponse({'data':status})



def edit_address(request,*args,**kwrgs):
    try:
        address_id = request.POST.get('id', None)
        name = request.POST.get('address_name', None)
        phone_no = request.POST.get('address_phone_no', None) 
        pincode = request.POST.get('address_pincode', None) 
        locality = request.POST.get('address_locality', None)
        address = request.POST.get('address_address', None)
        city_district_town = request.POST.get('address_city_district_town', None) 
        state = request.POST.get('state', None) 
        landmark = request.POST.get('address_landmark', None)
        alt_phone_no = request.POST.get('address_alt_phone_no', None) 
        address_type = request.POST.get('edit_addresstype', None) 
        useraddress=UserAddress.objects.get(pk=address_id)
        useraddress.name=name
        useraddress.phone_no=phone_no
        useraddress.pincode=pincode
        useraddress.locality=locality
        useraddress.address=address
        useraddress.city_district_town=city_district_town
        useraddress.state=state
        if len(landmark)>0:
            useraddress.landmark=landmark
        if len(alt_phone_no)>0:
            useraddress.alt_phone_no=alt_phone_no
        useraddress.address_type=address_type
        useraddress.modified_id=request.user
        useraddress.modified_ip=get_client_ip(request)
        useraddress.record_status='modified'
        useraddress.save()
        status=True
    except:
        status=False
    return JsonResponse({'data':status})
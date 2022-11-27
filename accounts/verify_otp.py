
from django.conf import settings

from twilio.rest import Client
from django.http import JsonResponse


from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .models import User,VerificationUser

# Create your views here.

def send_otp(mobile,user_instence):
    number= '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id=settings.SERVICES_ID
    client = Client(account_sid, auth_token)
    verification = client.verify \
                        .services(service_id) \
                        .verifications \
                        .create(to=number, channel='sms')
                        
    if VerificationUser.objects.filter(user=user_instence).exists():
        user=get_object_or_404(VerificationUser,user=user_instence)
        print(user)
        user.otp_attempt+=1
        user.save()
    else:
        user=VerificationUser()
        user.user=user_instence
        user.otp_attempt+=1
        user.save()
    print(verification.sid)
    return  user.id


def verify_otp(mobile,otp):
    number= '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id=settings.SERVICES_ID
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
                        .services(service_id) \
                        .verification_checks \
                        .create(to=number, code=otp)

    print(verification_check.status)
    if verification_check.status=='approved':
        print('verification confirm')
        return True
    else:
        return False
    
    
    
def otp_verify_code(request,phone_no,uid,verification_user):
    try:
        if  request.method == 'POST':
            otp = request.POST['otp']
            verify=verify_otp(phone_no,otp)
            if  verify: 
                user=User.objects.get(pk=uid)
                user.is_active = True
                user.save()
                user_verifcation=VerificationUser.objects.get(pk=verification_user)
                user_verifcation.otp=otp
                user_verifcation.otp_verification=True
                user_verifcation.save()
                login(request,user)
                return redirect('landing:landing_page')
            else:
                messages.error(request,'invalid otp recheck')
                return redirect('accounts:registration')
        context={
            'phone_no':phone_no,
            'uid':uid,
            'verification_user':verification_user
        }
        return render(request,'user/accounts/otp-verify.html',context)
    except:
        return render(request,'user/status/404.html')


def resent_otp(request):
    phone_no=request.GET.get('phone_no', None)
    uid=request.GET.get('uid', None)
    user_instence=get_object_or_404(User,pk=uid)
    # verification_user=get_object_or_404(VerificationUser,user=user_instence)
    send_otp(phone_no,user_instence)
    data={
        'status': True
    }
    print(data['status'])
    return JsonResponse(data)





def admin_send_otp(mobile):
    number= '+91'+str(mobile)
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    service_id=settings.SERVICES_ID
    client = Client(account_sid, auth_token)
    verification = client.verify \
                        .services(service_id) \
                        .verifications \
                        .create(to=number, channel='sms')
    print(verification.sid)
    return  verification.sid
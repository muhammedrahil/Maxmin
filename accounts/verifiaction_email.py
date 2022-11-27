from django.shortcuts import redirect
from django.contrib.auth import login
from .models import User,VerificationUser
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def activate_email(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid) 
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        user_verifcation=VerificationUser()
        user_verifcation.user=user
        user_verifcation.email_verification=True
        user_verifcation.save()
        login(request,user)
        return redirect('landing:landing_page')
    else:
        return redirect('accounts:registration')
    
    
def Reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid) 
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        return redirect('accounts:Reset_password',uid=uid)
    else:
        return redirect('accounts:forget_password')
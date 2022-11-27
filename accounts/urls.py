from django.urls import path
from . import views as v
from . import verifiaction_email as verification
from . import verify_otp as otp
from . import account_deatails as a
from . import admin_users as au

app_name = 'accounts'


urlpatterns = [
    path('login',v.user_login,name='login'),
    path('registration',v.user_registration,name='registration'),
    path('activate/<uidb64>/<token>',verification.activate_email,name='activate_email'),
    path('check_mail',v.check_mail,name='check_mail'),
    path('otp-verify/<int:phone_no>/<int:uid>/<int:verification_user>',otp.otp_verify_code,name='otp_verify_code'),
    path('resent-otp',otp.resent_otp,name='resent_otp'),
    path('logout',v.user_logout,name='logout'),
    path('forget-password',v.forget_password,name='forget_password'),
    path('Reset-password-validate/<uidb64>/<token>',verification.Reset_password_validate,name='Reset_password_validate'),
    path('Reset-password/<int:uid>',v.Reset_password,name='Reset_password'),
    
    path('',a.accounts,name='accounts'),
    path('user-infermations',a.user_infermations,name='user_infermations'),
    path('user-address-deatails',a.user_address_deatails,name='user_address_deatails'),
    
    path('delete-user-address',a.delete_address,name='delete_address'),
    path('edit-user-address',a.edit_address,name='edit_address'),
    
    path('user-list',au.user_list,name='user_list'),
    path('admin-user-address/<str:pk>',au.admin_user_address,name='admin_user_address'),
    path('block-user',au.block_user,name='block_user'),
    path('Active_user',au.Active_user,name='Active_user'),

    
    path('maxmin-admin',v.maxmin_admin,name='maxmin_admin'),
    path('maxmin-admin-opt/<int:phone_no>/<int:uid>',v.maxmin_admin_otp,name='maxmin_admin_otp'),
    
    path('maxmin-admin-logout',v.admin_logout,name='admin_logout'),
    

    
    
    
    
    
    
    
    
    
]
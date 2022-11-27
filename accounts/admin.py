from django.contrib import admin

# Register your models here.
from .models import User,VerificationUser,UserAddress
from django.contrib.auth.admin import UserAdmin


class UserAccounts(UserAdmin):
    list_display = ('id','email','phone_no','first_name','last_name','gender','is_active','is_superadmin','created_date','modified_date','record_status')
    filter_horizontal=[]
    list_filter=[]
    fieldsets = []
    search_fields=['email']
    ordering =()
    list_display_links =['email','first_name']
    list_filter =['email']

admin.site.register(User,UserAccounts)

@admin.register(VerificationUser)
class VerificationUserAdmin(admin.ModelAdmin):
    list_display = ['user','otp','otp_verification','email_verification','otp_attempt','otp_sent_date','verification_date']
    
    
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','phone_no','pincode','locality','address','city_district_town','state','landmark','alt_phone_no','address_type','created_date']
    
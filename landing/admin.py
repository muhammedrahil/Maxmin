from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
        list_display = ['product','banner','mainbanner','small_banner','centerbanner','hero_banner','created_date','modified_date','is_active']
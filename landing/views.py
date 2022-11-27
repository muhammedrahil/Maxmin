import random
from django.shortcuts import render
from .models import Advertisement
from product.models import *
# Create your views here.
from datetime import datetime,timedelta




def landing_page(request,*args,**kwargs):
    date=datetime.now()-timedelta(30)
    advertisement = Advertisement.objects.filter(small_banner=True,is_active=True).filter(created_date__gte=date).order_by('?')[:4]
    main_advertisement = Advertisement.objects.filter(mainbanner=True,is_active=True).filter(created_date__gte=date).order_by('?')
    center_advertisement = Advertisement.objects.filter(centerbanner=True,is_active=True).filter(created_date__gte=date).order_by('?')
    try:
        center_advertisement=random.sample(list(center_advertisement),2)
    except:
        pass
    try:
        main_advertisement=random.choice(main_advertisement)
    except:
        pass
    hero_banner_advertisement = Advertisement.objects.filter(hero_banner=True,is_active=True).order_by('-created_date')
    
    product=SubProductAttribute.objects.select_related(
            'product').filter(product__is_active=True,is_active=True).order_by('-created_date').order_by('?')[:8]
    context={
        'advertisement':advertisement,
        'main_advertisement':main_advertisement,
        'products':product,
        'center_advertisement':center_advertisement,
        'hero_banner_advertisement':hero_banner_advertisement
    }
    return render(request,'user/landing-page/max-min.html',context)


    
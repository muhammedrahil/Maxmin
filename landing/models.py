from django.db import models
from django.urls import reverse
from product.models import *

# Create your models here.


class Advertisement(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='advertisement_product')
    banner =  models.ImageField(upload_to='Advertisement/', null=True, blank=True,)
    mainbanner= models.BooleanField(default=False)
    centerbanner= models.BooleanField(default=False)
    hero_banner= models.BooleanField(default=False)
    small_banner=models.BooleanField(default=False)
    created_date        =   models.DateTimeField(auto_now_add=True)
    created_id          =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='add_created_id')
    created_ip          =   models.GenericIPAddressField(null=True, blank=True,)
    modified_date       =   models.DateTimeField(auto_now=True)
    modified_id         =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='add_modified_id')
    modified_ip         =   models.GenericIPAddressField(null=True, blank=True,)
    record_status       =   models.CharField(max_length=255,default='created')
    is_active           =   models.BooleanField(default=True)
    
    def get_absalute_url(self):
        s=self.product.main_category
        l=[]
        for i in s.all():
            l.append(i.pk)
        return reverse('product:allcategories', args=[self.product.category.id,self.product.slug,l[0]])


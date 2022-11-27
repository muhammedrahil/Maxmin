from django.db import models

import random
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    # print(base_name,' basename') #20210623_181743.jpg  basename
    ext = os.path.splitext(base_name)
    # print(ext,' extention')  #('20210623_181743', '.jpg')  extention
    return ext

# Create your models here.
# from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey

from django.conf import settings
User=settings.AUTH_USER_MODEL

class Category(MPTTModel):
    category        =   models.CharField(max_length=255,db_index=True)
    parent          =   TreeForeignKey('self',blank=True,null=True,related_name='child',on_delete=models.CASCADE)
    slug            =   models.SlugField(max_length=255)
    description     =   models.TextField(blank=True,null=True)
    is_active       =   models.BooleanField(default=True)
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='Category_created_id')
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_date   =   models.DateTimeField(auto_now=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='Category_modified_id')
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created')    

    class MPTTMeta:
        order_insertion_by = ['category']
        
    def __str__(self):                           
        return self.category
        
        
        
    # def __str__(self):                           
    #     full_path = [self.category]            
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.category)
    #         k = k.parent
    #     return ' -> '.join(full_path[::-1])

    class Meta:
        verbose_name_plural = 'categories'

    # def get_absolute_url(self): 
    #     return reverse('productsCategory:categories', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
        return super().save(*args, **kwargs)
   
    
class Size(models.Model):
    category            =   models.ForeignKey(Category,on_delete=models.CASCADE,null=True, blank=True,related_name='product_category_size')
    Size                =   models.CharField(max_length=300)
    slug                =   models.SlugField(max_length=255,null=True, blank=True,)
    discription         =   models.TextField(blank=True,null=True)
    is_active           =   models.BooleanField(default=True)
    created_date        =   models.DateTimeField(auto_now_add=True)
    created_id          =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='Size_created_id')
    created_ip          =   models.GenericIPAddressField(null=True, blank=True,)
    modified_date       =   models.DateTimeField(auto_now=True)
    modified_id         =   models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name='Size_modified_id')
    modified_ip         =   models.GenericIPAddressField(null=True, blank=True,)
    record_status       =   models.CharField(max_length=255,default='created')


    def __str__(self):
        return self.Size

    class Meta:
        verbose_name_plural = 'Size'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Size)
        return super().save(*args, **kwargs)



def brands_upload_image_path(instance, filename):    
    new_filename = random.randint(1,3910209312)
    # print(new_filename,' random')  # like -> 2727979836  random
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    # print(final_filename,' final_filename')  #2727979836('20210623_181743', '.jpg')  final_filename
    return "brands/{instance}/{new_filename}/{final_filename}".format(
            instance=instance,
            new_filename=new_filename, 
            final_filename=final_filename
            )
    
class Brand(models.Model):
    brand_category      =   models.ManyToManyField(Category,related_name='brand_category')
    title               =   models.CharField(max_length=300)
    slug                =   models.SlugField(max_length=255,null=True, blank=True,)
    brand_images        =   models.ImageField(upload_to=brands_upload_image_path, null=True, blank=True,)
    discription         =   models.TextField(blank=True,null=True)
    is_active           =   models.BooleanField(default=True)
    created_date        =   models.DateTimeField(auto_now_add=True)
    created_id          =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='Brand_created_id',null=True, blank=True)
    created_ip          =   models.GenericIPAddressField(null=True, blank=True)
    modified_date       =   models.DateTimeField(auto_now=True)
    modified_id         =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='Brand_modified_id',null=True, blank=True)
    modified_ip         =   models.GenericIPAddressField(null=True, blank=True)
    record_status       =   models.CharField(max_length=255,default='created')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'brands'   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    
    
    
class Color(models.Model):
    title               =   models.CharField(max_length=300,null=True, blank=True)
    color_code          =   models.CharField(max_length=200,null=True, blank=True)
    slug                =   models.SlugField(max_length=255,unique=True,null=True, blank=True,)
    discription         =   models.TextField(blank=True,null=True)
    is_active           =   models.BooleanField(default=True)
    created_date        =   models.DateTimeField(auto_now_add=True)
    created_id          =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='color_created_id',null=True, blank=True)
    created_ip          =   models.GenericIPAddressField(null=True, blank=True)
    modified_date       =   models.DateTimeField(auto_now=True)
    modified_id         =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='color_modified_id',null=True, blank=True)
    modified_ip         =   models.GenericIPAddressField(null=True, blank=True)
    record_status       =   models.CharField(max_length=255,default='created',null=True, blank=True)


    def __str__(self):
        return f"{self.title} {self.color_code}"

    class Meta:
        verbose_name_plural = 'color'   

    def save(self,*args, **kwargs):
        if not self.slug:
            slug=self.title,self.color_code
            self.slug = slugify(slug)
        return super().save(*args, **kwargs)
    
    
class GenderCategory(models.Model):
    gender              =   models.CharField(max_length=255,blank=True,null=True) 
    is_active           =   models.BooleanField(default=True)
    created_date        =   models.DateTimeField(auto_now_add=True)
    created_id          =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='gender_created_user',null=True, blank=True)
    created_ip          =   models.GenericIPAddressField(null=True, blank=True)
    modified_date       =   models.DateTimeField(auto_now=True)
    modified_id         =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='gender_modifide_user',null=True, blank=True)
    modified_ip         =   models.GenericIPAddressField(null=True, blank=True)
    record_status       =   models.CharField(max_length=255,default='created',null=True, blank=True)
    
    def __str__(self):
        return self.gender
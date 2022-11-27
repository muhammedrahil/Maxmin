
from email.mime import image
from email.policy import default
from django.db import models
import random
import os
from category.models import *
from django.urls import reverse


# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    # print(base_name,' basename') #20210623_181743.jpg  basename
    ext = os.path.splitext(base_name)
    # print(ext,' extention')  #('20210623_181743', '.jpg')  extention
    return ext



def upload_image_path(instance, filename):
    print(filename,' filename')
    print(instance,' instance')
    
    new_filename = random.randint(1,3910209312)
    # print(new_filename,' random')  # like -> 2727979836  random
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    # print(final_filename,' final_filename')  #2727979836('20210623_181743', '.jpg')  final_filename
    return "products/{instance}/{new_filename}/{final_filename}".format(
            instance=instance,
            new_filename=new_filename, 
            final_filename=final_filename
            )



#*************************** category choice ********************************

CHOICES = [
    ('1', 'Man'),
    ('2', 'Woman'),
    ('3', 'Kids'),
]

#*************************** product table  ********************************

class Product(models.Model):
    category        =   models.ForeignKey(Category,null=True, blank=True,on_delete=models.CASCADE,related_name='product_reference_sub_category',)
    product_brand   =   models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='product_reference_brand',blank=True,null=True)
    main_category   =   models.ManyToManyField(GenderCategory,related_name='product_reference_gender')
    product_name    =   models.CharField(max_length=255,blank=True,null=True)
    main_image      =   models.ImageField(upload_to=upload_image_path, null=True, blank=True,)
    slug            =   models.SlugField(max_length=255,blank=True,null=True)
    unit_price      =   models.DecimalField(decimal_places=2,max_digits=8,blank=True,null=True)
    description     =   models.TextField(blank=True,null=True)
    rating              =   models.IntegerField(default=0)
    product_totel_stoke = models.IntegerField(blank=True,null=True,default=0)
    is_active       =   models.BooleanField(default=True)
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='Products_created_id',blank=True,null=True)
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_date   =   models.DateTimeField(auto_now=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='Products_modified_id',blank=True,null=True)
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created',blank=True,null=True)  
      

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Product'
        ordering = ('-created_date',)
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug=self.product_name,self.pk
            self.slug = slugify(slug)
        return super().save(*args, **kwargs)   



def sub_upload_image_path(instance, filename):
    print(filename,' filename')
    print(instance,' instance')
    
    new_filename = random.randint(1,3910209312)
    # print(new_filename,' random')  # like -> 2727979836  random
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    # print(final_filename,' final_filename')  #2727979836('20210623_181743', '.jpg')  final_filename
    return "sub_products/{instance}/{new_filename}/{final_filename}".format(
            instance=instance,
            new_filename=new_filename, 
            final_filename=final_filename
            )

class SubProductAttribute(models.Model):
    product     = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='sub_product_reference_main_product')
    images      = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    images2     = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    images3     = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    images4     = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    images5     = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    images6     = models.ImageField(upload_to=sub_upload_image_path, null=True, blank=True,)
    sub_product_totel_stoke = models.IntegerField(blank=True,null=True,default=0)
    sku             =   models.CharField(max_length=355,blank=True,null=True,unique=True)
    product_color = models.ForeignKey(Color,on_delete=models.CASCADE,related_name='attribute_color_reference_sub_product')
    offerprice       =   models.DecimalField(decimal_places=2,max_digits=8)
    offer_persentage     =   models.FloatField(blank=True,null=True)
    offer_expiry_date    =  models.DateTimeField(blank=True,null=True)
    rating              =   models.IntegerField(default=0)
    is_active       =   models.BooleanField(default=True)
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_created_id',blank=True,null=True)
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_date   =   models.DateTimeField(auto_now=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_modified_id',blank=True,null=True)
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created',blank=True,null=True)  
    
    def __str__(self):
        return '{} {}'.format(self.product.product_name,self.pk)

    class Meta:
        verbose_name_plural = 'sub Product Attribute'


    def save(self, *args, **kwargs):
        self.offer_persentage = round((100-(self.offerprice / self.product.unit_price)*100),2)
        return super().save(*args, **kwargs)

    def get_absolute_url(self): 
        return reverse('product:single_Productdeatail', args=[self.product.slug,self.pk])



  


class ProductQuantity(models.Model):
    product     =   models.ForeignKey(SubProductAttribute,on_delete=models.CASCADE,related_name='Product_Quantity_referece_offer_product')
    product_size =  models.ForeignKey(Size,on_delete=models.CASCADE,related_name='attribute_size_reference_sub_product')
    quantity    =   models.IntegerField(default=1)
    stock        =   models.IntegerField(default=1)
    is_active       =   models.BooleanField(default=True)
    created_date    =   models.DateTimeField(auto_now_add=True)
    created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_quantity_created_id',blank=True,null=True)
    created_ip      =   models.GenericIPAddressField(blank=True,null=True)
    modified_date   =   models.DateTimeField(auto_now=True)
    modified_id     =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_quantity_modified_id',blank=True,null=True)
    modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
    record_status   =   models.CharField(max_length=255,default='created',blank=True,null=True)  
    class Meta:
        verbose_name_plural = 'Product Quantity'

    def __str__(self):
        return '{} ({})'.format(self.product,self.product.product.product_name)


def review_upload_image_path(instance, filename):
    print(filename,' filename')
    print(instance,' instance')
    
    new_filename = random.randint(1,3910209312)
    # print(new_filename,' random')  # like -> 2727979836  random
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    # print(final_filename,' final_filename')  #2727979836('20210623_181743', '.jpg')  final_filename
    return "review/{instance}/{new_filename}/{final_filename}".format(
            instance=instance,
            new_filename=new_filename, 
            final_filename=final_filename
            )
    

class ProductReview(models.Model):
        product     =   models.ForeignKey(SubProductAttribute,on_delete=models.CASCADE,related_name='Product_review_referece_offer_product')
        rating      =   models.IntegerField(null=True, blank=True,)
        subject     =   models.CharField(max_length=255,blank=True,null=True)
        description     =   models.TextField(blank=True,null=True)
        product_image   =   models.ImageField(upload_to=review_upload_image_path, null=True, blank=True,)
        is_active       =   models.BooleanField(default=True)
        created_date    =   models.DateTimeField(auto_now_add=True)
        created_id      =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_review_created_id',blank=True,null=True)
        created_ip      =   models.GenericIPAddressField(blank=True,null=True)
        modified_date   =   models.DateTimeField(auto_now=True)
        modified_id     =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub_Products_review_modified_id',blank=True,null=True)
        modified_ip     =   models.GenericIPAddressField(blank=True,null=True)
        record_status   =   models.CharField(max_length=255,default='created',blank=True,null=True) 

        def __str__(self):
            return '{} ({})'.format(self.product,self.rating)

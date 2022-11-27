from django.shortcuts import render,get_object_or_404
from category.models import *
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)


def all_categories(request,*args,**kwargs):
    category = get_object_or_404(Category,pk=kwargs.get('pk')) 
    genter= kwargs.get('genter')
    try:
        if category.level == 0:
            product=SubProductAttribute.objects.select_related(
            'product','product__category',).filter(product__is_active=True,product__main_category=genter,product__category__parent_id=category.id,is_active=True)
            subcategory= Category.objects.filter(parent_id=category)
            brands= Brand.objects.filter(brand_category=category)
            size= Size.objects.filter(category=category)
            main_category = category.pk
        else:
            product=SubProductAttribute.objects.select_related(
            'product','product__category',).filter(product__is_active=True,product__main_category=genter,product__category=category,is_active=True)
            subcategory= Category.objects.filter(parent_id=category.parent_id)
            brands= Brand.objects.filter(brand_category=category.parent_id)
            size= Size.objects.filter(category=category.parent_id)
            main_category = category.parent_id
        lenght_product=False
        if len(product) > 0:
            lenght_product=True
        color= Color.objects.all()
        paginator = Paginator(product, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context =   {
            'maincategory':main_category,
            'subcategory':subcategory,
            'products' : page_obj,
            'brands': brands,
            'size':size,
            'color':color,
            'lenght_product':lenght_product
        }
        return render(request,'user/products/products.html',context)
    except SubProductAttribute.DoesNotExist:
        return render(request,'user/status/404.html')


def filter_data(request):
    try:
        categories=request.GET.getlist('subcategory[]')
        brands=request.GET.getlist('brand[]')
        sizes=request.GET.getlist('size[]')
        color=request.GET.getlist('color[]')
        main_category=request.GET['category_id']
        allProduct=SubProductAttribute.objects.select_related(
            'product','product__category',).filter(product__is_active=True,product__category__parent_id=main_category).filter(is_active=True)
        
        if len(categories)>0:
            allProduct=allProduct.filter(product__category__id__in=categories)
        if len(brands)>0:
            allProduct=allProduct.filter(product__product_brand__id__in=brands)
        if len(color)>0:
            allProduct=allProduct.filter(product_color__id__in=color)
        if len(sizes)>0:
            sizeproduct=ProductQuantity.objects.filter(product_size__id__in=sizes)
            product = [ c.product for c in sizeproduct]
            product = [ c.id for c in product]
            allProduct=allProduct.filter(id__in=product)
        template =render_to_string('user/products/filter-data.html',{'data':allProduct})
        return JsonResponse({'data':template})  
    except:
        pass    

def filterprice(request,*args,**kwargs):
    min=request.POST.get('min')
    max=request.POST.get('max')
    main_category=request.POST.get('category_id')
    
    allProduct=SubProductAttribute.objects.select_related(
        'product','product__category',).filter(product__is_active=True,product__category__parent_id=main_category).filter(is_active=True)
    if len(min)>0:
        allProduct=allProduct.filter(offerprice__gte=min)
    if len(max)>0:
        allProduct=allProduct.filter(offerprice__lte=max)
    print(allProduct)
    template =render_to_string('user/products/filter-data.html',{'data':allProduct})
    return JsonResponse({'data':template}) 

# @cache_page(60 * 1500)
def single_Productdeatail(request,*args,**kwargs):
    try:
        # del request.session['cartdata']
        # del request.session['length_product']
        pk=kwargs.get('single_Productdeatail_pk')
        slug=kwargs.get('product_slug')
        
        # if cache.get([pk,slug]):
        #     try:
        #         print("DATA COMING FROM CACHE")
        #         context = cache.get([pk,slug])
        #         # cache.delete([pk,slug])
        #     except:
        #         print("DATA COMING FROM DB")
        #         product=SubProductAttribute.objects.get(pk=pk,is_active=True)
        #         related_product=SubProductAttribute.objects.filter(product__slug=slug,is_active=True).exclude(pk=pk)
        #         product_qwantity  = ProductQuantity.objects.filter(product=product,is_active=True)
        #         producy_review=ProductReview.objects.filter(product=product)
        #         related_products=SubProductAttribute.objects.select_related(
        #             'product','product__category',).filter(product__is_active=True,product__category=product.product.category).filter(is_active=True)
        #         context={
        #         'product':product,
        #         'related':related_product,
        #         'product_qwantity':product_qwantity,
        #         'producy_review':producy_review,
        #         'related_products':related_products
                
        #         }
        #         cache.set([pk,slug], context)
                
        # else:
        print("DATA COMING FROM DB")
        product=SubProductAttribute.objects.get(pk=pk,is_active=True)
        related_product=SubProductAttribute.objects.filter(product__slug=slug,is_active=True).exclude(pk=pk)
        product_qwantity  = ProductQuantity.objects.filter(product=product,is_active=True)
        producy_review=ProductReview.objects.filter(product=product)
        producy_review_count=producy_review.count()
        related_products=SubProductAttribute.objects.select_related(
            'product','product__category',).filter(product__is_active=True,product__category=product.product.category).filter(is_active=True)[:4]
        context={
        'product':product,
        'related':related_product,
        'product_qwantity':product_qwantity,
        'producy_review':producy_review,
        'related_products':related_products,
        'producy_review_count':producy_review_count,
        }
            # cache.set([pk,slug], context)
            
        return render(request,'user/single-product-section/single-product.html',context)
    except:
        return render(request,'user/status/404.html')


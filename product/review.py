from django.shortcuts import redirect, render,get_object_or_404
from .forms import ProductReviewForm
from .models import ProductReview,SubProductAttribute,Product
from cart.order import get_client_ip

def product_review(request,*args,**kwargs):
  pk=kwargs.get('pk')
  if request.method == 'POST':
    product=get_object_or_404(SubProductAttribute,pk=pk)
    rating= request.POST.get('rating')
    form=ProductReviewForm(request.POST,request.FILES)
    if form.is_valid():     
      subject=form.cleaned_data['subject']
      description=form.cleaned_data['description']
      product_image=form.cleaned_data['product_image']
      review=ProductReview()
      review.product=product
      review.rating=rating
      if subject != None: 
        review.subject=subject
      if description != None: 
        review.description=description
      if product_image != None:
        review.product_image=product_image
      review.created_id=request.user
      review.created_ip=get_client_ip(request)
      review.save()
      producy_review=ProductReview.objects.filter(product=product)
      producy_review_count=producy_review.count()
      fullReview_rate=producy_review_count*5
      product_rateing=0
      for i in producy_review:
          product_rateing+=i.rating
      rateing=(product_rateing/fullReview_rate)*100
      totelstar=(5/100)*rateing
      product.rating=totelstar
      product.modified_id=request.user
      product.modified_ip=get_client_ip(request)
      product.record_status='modified'
      product.save()
      
      main_product=get_object_or_404(Product,pk=product.product.pk)
      producy_rating_obj=SubProductAttribute.objects.filter(product=main_product,rating__gte=1)
      producy_rating_obj_count=producy_rating_obj.count()
      producy_rating_obj_fullReview_rate=producy_rating_obj_count*5
      sub_producy_rating=0
      for i in producy_rating_obj:
         sub_producy_rating += i.rating
      sub_rateing=(sub_producy_rating/producy_rating_obj_fullReview_rate)*100
      sub_totelstar=(5/100)*sub_rateing
      main_product.rating=sub_totelstar
      main_product.modified_id=request.user
      main_product.modified_ip=get_client_ip(request)
      main_product.record_status='modified'
      main_product.save()
      return redirect('payment:order_deatails')
  form=ProductReviewForm()
  context={
    'form':form
  }
  return render(request,'user/review/review.html',context)
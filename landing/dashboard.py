from django.shortcuts import render
from payment.models import Payment
from django.db.models import Sum
from accounts.models import VerificationUser
from product.models import SubProductAttribute
from category.models import Category as Cat
from django.db.models import Count,Sum
from django.db.models.functions import ExtractMonth
import calendar
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_control,never_cache


@staff_member_required(login_url='accounts:maxmin_admin')
@never_cache
def dashboard(request,*args,**kwargs):
    try:
        category = Cat.objects.filter(is_active=True)
        category_count=category.filter(level=0).count()
        product_list=SubProductAttribute.objects.filter(is_active=True)
        product_count=product_list.count()
        order_list=Payment.objects.select_related('order_status','order_status__order').filter(order_status__order__is_active=True)
        totel_sales=order_list.filter(order_status__delivered=True).count()
        revenue=order_list.exclude(order_status__Cancelled=True).filter(payment_complete_status=True).aggregate(Sum('payment_price'))
        totel_order=order_list.count()
        user=VerificationUser.objects.select_related('user').filter(user__is_active=True).exclude(user__is_superadmin=True)
        user_count=user.count()
        category_list=SubProductAttribute.objects.values('product__category__parent_id__category').annotate(cat=Count('product__category__parent_id'))
        category_name=[]
        category_counts=[]
        for i in category_list:
            category_name.append(i['product__category__parent_id__category'])
            category_counts.append(i['cat'])
        order_payment_list=Payment.objects.values('order__products__product__product__category__parent_id__category').annotate(
            sum=Sum('order__products__totel_qty_price')).exclude(order_status__Cancelled=True).exclude(payment_status='PENDING')
        payment_category_name=[]
        payment_category_amount=[]
        for i in order_payment_list:
            payment_category_name.append(i['order__products__product__product__category__parent_id__category'])
            payment_category_amount.append(float(i['sum']))
            
        month_payment= Payment.objects.values('payment_price').annotate(month=ExtractMonth('payment_date')).values('month').annotate(
            sum=Sum('payment_price')).exclude(payment_status='PENDING') 
        month_payment_month=[]
        month_payment_amount=[]
        for i in month_payment:
            month_payment_month.append(calendar.month_name[i['month']])
            month_payment_amount.append(float(i['sum']))  
        context={
            'revenue':revenue,
            'user_count':user_count,
            'totel_order':totel_order,
            'product_count':product_count,
            'totel_sales':totel_sales,
            'category_count':category_count,
            'category_name':category_name,
            'category_counts':category_counts,
            'payment_category_name':payment_category_name,
            'payment_category_amount':payment_category_amount,
            'month_payment_month':month_payment_month,
            'month_payment_amount':month_payment_amount
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        return render(request,'admin_/dashboard/dashboard.html',context)
    except:
        return render(request,'massages/404.html')
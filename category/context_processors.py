
from category.models import Category as CategoryModel,GenderCategory as GenderCategoryModel
from cart.models import Cart


def category(request,*args,**kwargs):
    cart_products=[]
    subtotel=0
    if request.user.is_authenticated :
        cart_products=Cart.objects.filter(user=request.user).filter(is_active=True)
        for i in cart_products:
            subtotel+=i.totel_qty_price
    # print(cart_products)
    context={
        'context_category': CategoryModel.objects.filter(is_active=True), 
        'gender_category': GenderCategoryModel.objects.filter(is_active=True),
        'cart_products':cart_products,
        'subtotel':subtotel,
    }
    if 'cartdata' in request.session:
        # del request.session['cartdata']
        cart_data=request.session['cartdata']
        subtotel=0
        for i in cart_data:
            subtotel+=float(cart_data[i]['sub_totel_price'])
        context.update({'cart_data':cart_data})
        context.update({'subtotel':subtotel})
        # print(cart_data)
    return context  

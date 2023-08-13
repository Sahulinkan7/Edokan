from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from store.models import Product,Variation
from .models import Cart,Cart_item
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
    
def add_to_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variations=[]
    if request.method=='POST':
        for item in request.POST:
            key = item
            value= request.POST[key]
                       
            try:
               variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
               product_variations.append(variation)
            except:
                pass
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cart_item=Cart_item.objects.get(product=product,cart=cart)
        if len(product_variations)>0:
            cart_item.variation.clear()
            for item in product_variations:
                cart_item.variation.add(item)
        cart_item.quantity += 1 
        cart_item.save()
    except Cart_item.DoesNotExist:
        cart_item=Cart_item.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if len(product_variations)>0:
            cart_item.variation.clear()
            for item in product_variations:
                cart_item.variation.add(item)
        cart_item.save()
    return redirect("cart")

def remove_from_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_item.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")

def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item= Cart_item.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect("cart")
    
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(total*5/100)
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    
    context={
        'total':total,
        'quantity':quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,"carts/cart.html",context)
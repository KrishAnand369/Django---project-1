from django.http import JsonResponse
from django.shortcuts import redirect,render
from store.models import Product, MyFoodFiesta
from django.contrib.auth.decorators import login_required

def addToCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id =prod_id)
            if(product_check):
                if(MyFoodFiesta.objects.filter(user = request.user.id,product_id=prod_id)):
                    return JsonResponse({'status':'Product already in Cart'})
                else:
                    prod_qty =int(request.POST.get('product_qty'))
                    if product_check.quantity >=prod_qty:
                        MyFoodFiesta.objects.create(user = request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':'Product added successfully'})
                    else:
                        return JsonResponse({'status':'only '+str(product_check.quantity)+'quantity available'})
            else:
                return JsonResponse({'status':'No Such product Found'})
        else:
            return JsonResponse({'status':'Login to Continue'})
    return redirect('/')

@login_required(login_url='loginpage')
def viewCart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = MyFoodFiesta.objects.filter(user=user)
        context={'cart':cart}
        return  render(request,"store/cart.html",context)
    else:
        return  redirect('loginpage')


def updateCart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(MyFoodFiesta.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = MyFoodFiesta.objects.get(user=request.user,product_id=prod_id)
            cart.product_qty=prod_qty
            cart.save()
            return JsonResponse({'status':'updated Successfully'})


def deleteCartItem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(MyFoodFiesta.objects.filter(user=request.user,product_id=prod_id)):
            cartItem =MyFoodFiesta.objects.get(product_id=prod_id,user=request.user)
            cartItem.delete()
            return JsonResponse({'status':'Deleted Successfully'})
        else:
            return  JsonResponse({'status':'Item not found in Cart!'})
    return redirect('/')
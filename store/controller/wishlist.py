from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from store.models import Product, WishList
from django.http.response import JsonResponse

@login_required(login_url="loginpage")
def index(request):
    wishList = WishList.objects.filter(user=request.user)
    context = {'wishList':wishList}
    return render(request,'store/wishList.html',context)


def addToWishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(WishList.objects.filter(user=request.user,product_id=prod_id)):
                    return JsonResponse({'status':'Product already in Wishlist'})
                else:
                    WishList.objects.create(user=request.user,product_id=prod_id)
                    return JsonResponse({'status': 'Product added to WishList'})
            else:
                return JsonResponse({'status': 'No Such Product found'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('/')


def deleteWishlistItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                wishlist_item=WishList.objects.get(user=request.user,product_id=prod_id)
                wishlist_item.delete()
                return JsonResponse({'status': 'Product removed from WishList'})
            except WishList.DoesNoExist:
                return JsonResponse({'status': 'Product not found in WishList'})
        else:
            return JsonResponse({'status': 'Login to Continue'})
    return redirect('/')
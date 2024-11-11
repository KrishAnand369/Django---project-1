import random

from django.contrib.auth.models import User
from django.http import JsonResponse
from  django.shortcuts import  redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product, MyFoodFiesta, WishList, Order, OrderItem, Profile

@login_required(login_url='loginpage')
def index(request):
    rawCart = MyFoodFiesta.objects.filter(user=request.user)
    for item in rawCart:
        if item.product_qty > item.product.quantity:
            MyFoodFiesta.objects.delete(id=item.id)


    cartItem = MyFoodFiesta.objects.filter(user=request.user)
    total_price = 0;
    for item in cartItem:
        total_price += item.product.selling_price*item.product_qty

    userProfile = Profile.objects.filter(user=request.user).first()

    context={'cartItem':cartItem,'total_price':total_price,'userProfile':userProfile}
    return render(request,'store/checkout.html',context)

@login_required(login_url='loginpage')
def placeOrder(request):
    if request.method == 'POST':
        currentUser = User.objects.filter(id=request.user.id).first()

        if not currentUser.first_name:
            currentUser.first_name=request.POST.get('firstName')
            currentUser.last_name=request.POST.get('lastName')
            currentUser.email=request.POST.get('email')
            currentUser.save()

        if not Profile.objects.filter(user=request.user):
            userProfile = Profile()
            userProfile.user=request.user
            userProfile.phone=request.POST.get('phone')
            userProfile.address=request.POST.get('Address')
            userProfile.city=request.POST.get('city')
            userProfile.state=request.POST.get('state')
            userProfile.country=request.POST.get('country')
            userProfile.pinCode=request.POST.get('pinCode')
            userProfile.save()

        newOrder = Order()
        newOrder.user = request.user
        newOrder.fName = request.POST.get('firstName')
        newOrder.lName = request.POST.get('lastName')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.Address = request.POST.get('Address')
        newOrder.city = request.POST.get('city')
        newOrder.state = request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pinCode = request.POST.get('pinCode')

        newOrder.payment_mode=request.POST.get('payment_mode')
        newOrder.payment_id=request.POST.get('payment_mode')

        cart =MyFoodFiesta.objects.filter(user=request.user)
        cart_total_price =sum(item.product.selling_price* item.product_qty for item in cart)

        newOrder.total_price = cart_total_price
        trackno = 'OrderNo' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'OrderNo' + str(random.randint(1111111, 9999999))

        newOrder.tracking_no = trackno
        newOrder.save()

        for item in cart:
            OrderItem.objects.create(
                order = newOrder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )

        # Decrese the product quantity from available stock

            orderProduct = Product.objects.filter(id=item.product_id).first()
            orderProduct.quantity -= item.product_qty
            orderProduct.save()

        # clear user Cart
        MyFoodFiesta.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has been placed successfully")

        payMode = request.POST.get('payment_mode')
        if payMode == "Paid by Razorpay":
            return JsonResponse({'status': "Your order has been placed successfully & payment done"})
    return redirect('order/')


def razerpayCheck(request):
    cart = MyFoodFiesta.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price* item.product_qty

    return  JsonResponse({'total_price':total_price})
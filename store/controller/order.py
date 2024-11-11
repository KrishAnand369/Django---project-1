from lib2to3.fixes.fix_input import context

from django.contrib.auth.models import User
from django.http import JsonResponse
from  django.shortcuts import  redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product, MyFoodFiesta, WishList, Order, OrderItem, Profile


def orderView(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,'store/order.html',context)

def order_View(request,t_no):
    orders = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderItems = OrderItem.objects.filter(order=orders)
    context = {'orders':orders,'orderItems':orderItems}
    return render(request,'store/orderItem.html',context)
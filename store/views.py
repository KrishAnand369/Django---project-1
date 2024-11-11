from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import *


# Create your views here.
def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {'trending_products':trending_products}
    return render(request,"store/home.html",context)

def main(request):
    return render(request,"store/layouts/main.html")

def navbar(request):
    return  render(request,"store/inc/navbar.html")

def collections(request):
    category = Category.objects.filter(status = 0)
    context = {'category': category}
    return render(request,'store/collections.html',context)

def collectionsView(request,slug):
    if(Category.objects.filter(slug = slug,status = 0)):
        products =Product.objects.filter(category__slug = slug)
        category_name = Category.objects.filter(slug = slug).first()
        context = {"products":products,"category_name":category_name}
        return render(request,'store/products/home.html',context)
    else:
        messages.warning(request,"No such Category Found !!!")
        return  redirect("collections")



def productView(request,cate_slug,prod_slug):
    if Category.objects.filter(slug=cate_slug,status=0).exists():
        if Product.objects.filter(slug=prod_slug,status=0).exists():
            products=Product.objects.filter(slug=prod_slug,status=0).first()
            context={'products':products}
        else:
            messages.error(request,"No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"No Such Category Found")
        return redirect("collections")
    return render(request,'store/products/view.html',context)
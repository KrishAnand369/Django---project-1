from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from store.controller import authView, wishlist, myFoodFiesta, checkout, order

app_name ="store"
urlpatterns = [
    path(' ',views.home,name = 'home'),
    path('collections',views.collections,name = 'collections'),
    path('collections/<str:slug>',views.collectionsView,name = 'collectionsView'),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productView,name = 'productView'),

    path('register/',authView.register,name='register'),
    path('login/',authView.loginpage,name='loginpage'),
    path('logout/',authView.logoutpage,name = 'logoutPage'),

    path('add-to-cart',myFoodFiesta.addToCart,name='/add-to-cart'),
    path('cart',myFoodFiesta.viewCart,name='cart'),
    path('update-cart',myFoodFiesta.updateCart, name ='update-cart'),
    path('delete-cart-item',myFoodFiesta.deleteCartItem, name ='delete-cart-item'),

    path('wishlist',wishlist.index,name='wishlist'),
    path('add-to-wishlist',wishlist.addToWishlist,name='/add-to-wishlist'),
    path('delete-wishlist-item',wishlist.deleteWishlistItem,name='/delete-wishlist-item'),

    path('checkout',checkout.index,name='checkout'),
    path('placeOrder',checkout.placeOrder,name='placeOrder'),

    path('proceed-to-pay',checkout.razerpayCheck,name='proceed-to-pay'),
    path('order/',order.orderView,name='order'),
    path('view-order/<str:t_no>/',order.order_View,name='orderView'),
]

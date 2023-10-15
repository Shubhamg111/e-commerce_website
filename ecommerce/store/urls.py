from django.urls import path
from . import views
from store.controller import authview,cart,wishlist,checkout,order
urlpatterns=[
    path('',views.home,name="home"),
    path('collections',views.collections,name='collections'),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productview, name='productview'),

    path('register/',authview.register, name="register"),
    path('login/' ,authview.loginpage, name="loginpage"),
    path('logout/',authview.logoutpage, name="logoutpage"),
    path('cart-to-cart', cart.addtocart,name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart ,name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name='deletecartitem'),
    path('wishlist',wishlist.index, name="wishlist"),
    path('add-to-wishlist',wishlist.addtowishlist,name="addtowishlist"),
    path('delete-wishlist-item',wishlist.deletewishlistitem,name="deletewishlistitem"),
    path('checkout',checkout.index, name="checkout"),
    path('place-order',checkout.placeorder, name="placeorder"),
    path('orders',order.index, name="orders"),
    path('view-order/<str:t_no>',order.vieworder, name="orderview"),
    path('product-list',views.productlistajax),
    path('searchproducts',views.searchproducts,name="searchproducts"),

    path('esewa_verify',checkout.esewa_verify,name="esewaverify")
  



]
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Cart,Order,Product,OrderItem,Profile
from django.contrib.auth.models import User
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import User, Profile, Order, OrderItem, Product
import random

@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            item.delete()
            # Cart.objects.delete(id=item.id)

    cartitems =Cart.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price= total_price + item.product.selling_price * item.product_qty


    userprofile = Profile.objects.filter(user=request.user).first()

    context={
        'cartitems':cartitems,
        'total_price':total_price,
        'userprofile':userprofile

    }
    return render(request,"store/checkout.html",context)



@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
        currentuser = User.objects.filter(id=request.user.id).first()

        # Update user's first name and last name if not already set
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        # Create a user profile if it doesn't exist
        if not Profile.objects.filter(user=request.user).exists():
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        # Create a new order
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')

        # Calculate total price from the user's cart
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(item.product.selling_price * item.product_qty for item in cart)
        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        while True:
            trackno = 'Shubham' + str(random.randint(1111111, 9999999))
            if not Order.objects.filter(tracking_no=trackno).exists():
                break
        neworder.tracking_no = trackno

        neworder.save()
        for item in cart:
                order_item = OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty,
            )
   

        cartitems =Cart.objects.filter(user=request.user)
        total_price=0
        for item in cartitems:
            total_price= total_price + item.product.selling_price * item.product_qty

        # Get the selected payment method from the form data
        payment_mode = request.POST.get('payment_mode')

        if payment_mode == 'COD':
                 # Create order items and update product quantities
            
            # Handle COD payment method
                 # Decrease product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

            # Clear the user's cart
            cart.delete()

            messages.success(request, "Cash on Delivery selected. Order placed!")
            return redirect('/')  # Display a confirmation message on the same page
        elif payment_mode == 'Esewa':
            context={
                'order':neworder,
                'total_price':total_price,
                'cartitems':cartitems
            }
   # Handle COD payment method
                 # Decrease product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

            # Clear the user's cart
            cart.delete()
            # Handle Esewa payment method
            # You can pass any additional context data needed for the Esewa payment page
            return render(request, 'store/esewapayment.html',context)
        else:
            messages.error(request, "Something Went Wrong")
            return redirect('checkout')

    # Handle GET request or other cases
    return redirect('/')




# import requests as req
# import xml.etree.ElementTree as ET

#  # Import your Order and Cart models here

# def esewa_verify(request):
#     o_id = request.GET.get('o_id')
#     amounts = request.GET.get('amt')
#     refId = request.GET.get('refId')  # Corrected variable name
#     url = "https://uat.esewa.com.np/epay/main"

#     data = {
#         'amt': amounts,
#         'scd': 'EPAYTEST',
#         'rid': refId,
#         'pid': o_id
#     }

#     try:
#         resp = req.post(url, data)
#         print("status code=======", resp.status_code)

#         if resp.status_code == 200:
#             # Split the order_id and cart_id from the o_id
#             order_id, cart_id = o_id.split('_')

#             # Update the order's payment status
#             order = Order.objects.get(id=order_id)
#             order.payment_status = True
#             order.save()

#             # Delete the cart
#             cart = Cart.objects.get(id=cart_id)
#             cart.delete()

#             messages.add_message(request, messages.SUCCESS, 'Order success')
#             return redirect('orders')
#         else:
#             messages.add_message(request, messages.ERROR, 'Failed to order')
#             return redirect('/')
#     except Exception as e:
#         # Handle exceptions (e.g., network errors) here
#         messages.add_message(request, messages.ERROR, 'Failed to process payment')
#         return redirect('/')

#!/usr/bin/python3
import requests as req
import xml.etree.ElementTree as ET

def esewa_verify(request):
    o_id = request.GET.get('o_id')
    amounts = request.GET.get('amt')
    refId = request.GET.get('refId')
    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amounts,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': o_id
    }
    resp = req.post(url, d)
    print("status code=======", resp.status_code)

    if resp.status_code =='Success':
           # Split the order_id and cart_id from the o_id
            order_id, cart_id = o_id.split('_')

            # Update the order's payment status
            order = Order.objects.get(id=order_id)
            order.payment_status = True
            order.save()

            # Delete the cart
            cart = Cart.objects.get(id=cart_id)
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Order success')
            return redirect('orders')
    else:
            messages.add_message(request, messages.ERROR, 'Order Success')
            return redirect('/')
    
def orders(request):
    return render(request, 'store/orders/index.html')
from django.shortcuts import render,redirect
import requests
from .models import *
from django.http.response import JsonResponse

from django.contrib import messages
# Create your views here.

def home(request):
    trending_products=Product.objects.filter(trending=1)
    context={
        'trending_products':trending_products
    }
    return render(request,'store/index.html',context)

def collections(request):
    category =Category.objects.filter(status=0)
    context ={
        'category':category
        }
    return render(request,'store/collections.html',context)

def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category=Category.objects.filter(slug=slug).first()
        context={
            'products': products,
            'category': category
        }
        return render(request, "store/products/index.html",context)
    else:
        messages.warning(request,"No such category found")
        return redirect('collections')

def productview(request,cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products=Product.objects.filter(slug=prod_slug, status=0).first
            context={
                'products':products
            }
        else:
            messages.error(request,"no such category found")
            return redirect('collections')


    else:
        messages.error(request,"no such category found")
        return redirect('collections')
    return render(request,'store/products/view.html',context)

def productlistajax(request):
    category= Category.objects.filter(status=0).values_list('name',flat=True)
    # products = Product.objects.filter(status=0).values_list('name',flat=True)
    categorylist=list(category)
    # productslist=list(products)
    

    return JsonResponse(categorylist,safe=False)


# def searchproducts(request):
#     if request.method=='POST':
#        searchedterm=request.POST.get('productsearch') 
#        if searchedterm=="":
#            return redirect(request.META.get('HTTP_REFERER'))
#        else:
#            product=Product.objects.filter(name__contains=searchedterm).first()
#            category= Category.objects.filter(name__contains=searchedterm).first()


#            if product:
#                return redirect('collections/'+product.category.slug+'/'+product.slug)
#            if category:
#                return redirect('collections/'+ category.slug)
#            else:
#                messages.info(request,"No product matched your search")
#                return redirect(request.META.get('HTTP_REFERER'))

def searchproducts(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if not searchedterm:
            return redirect(request.META.get('HTTP_REFERER'))

        # products = Product.objects.filter(name__icontains=searchedterm)
        categories = Category.objects.filter(name__icontains=searchedterm)

        # if products.exists():
        #     # Handle multiple product matches here if needed.
        #     # For example, you can list all matching products.
        #     # Redirecting to the first match for simplicity.
        #     return redirect('collections/' + products.first().category.slug + '/' + products.first().slug)

        if categories.exists():
            # Handle multiple category matches here if needed.
            # For example, you can list all matching categories.
            # Redirecting to the first match for simplicity.
            return redirect('collections/' + categories.first().slug)

        messages.info(request, "No product or category matched your search")
        return redirect(request.META.get('HTTP_REFERER'))
               

    return redirect(request.META.get('HTTP_REFERER'))
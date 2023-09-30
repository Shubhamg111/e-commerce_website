from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem )
admin.site.register(Profile )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  # You can adjust the number of image upload fields shown

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
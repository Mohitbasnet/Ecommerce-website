from django.contrib import admin

from . models import Product,Cart,ProductInCart,Order

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(Order)

from django.contrib import admin

from . models import Product,Cart,ProductInCart,Order,Deal

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CartInline(admin.TabularInline):
    model = Cart  #onetoonefield foreign key

class DealInline(admin.TabularInline):
    model = Deal.user.through
    

class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'get_cart', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', ('is_active' , 'is_superuser'), )}),
        ('Important dates',{'fields': ('last_login', 'date_joined')}),
        #('Cart', {'fields': ('get_cart',)})
        ('Advanced options', {
            'classes': ('collapse',), #Advance options
            'fields': ('groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),   # class for css 
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}     # fields shown on create user page on admin panel
        ),
    )

    inlines = [
        CartInline, DealInline
    ]
    def get_cart(self,obj):       # this function only works in list_display
        return obj.cart           # through reverse related relationship
    search_fields = ('username',)     #search_filter for search bar
    ordering = ('username',)

admin.site.unregister(User)

admin.site.register(User,UserAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(Deal)
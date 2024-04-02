from django.contrib import admin

from . models import Product,Cart,ProductInCart,Order,Deal

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CartInline(admin.TabularInline):
    model = Cart  #onetoonefield foreign key

class DealInline(admin.TabularInline):
    model = Deal.user.through

class ProductInCartInline(admin.TabularInline):
    model = ProductInCart

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

@admin.register(Cart) # we can register cartadmin like this also
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user','staff', 'created_on',)    # here user__is_staff will not work   
    list_filter = ('user', 'created_on',)
    #fields = ('staff',)           # either fields or fieldset
    fieldsets = (
        (None, {'fields': ('user', 'created_on',)}),   # only direct relationship no nested relationship('__') ex. user__is_staff
        #('User', {'fields': ('staff',)}),
    )
    inlines = (
        ProductInCartInline,
    )
    # To display only in list_display
    def staff(self,obj):
        return obj.user.is_staff
    # staff.empty_value_display = '???'
    staff.admin_order_field  = 'user__is_staff'  #Allows column order sorting
    staff.short_description = 'Staff User'  #Renames column head

    #Filtering on side - for some reason, this works
    list_filter = ['user__is_staff', 'created_on',]    # with direct foreign key(user) no error but not shown in filters, with function error
    # ordering = ['user',]
    search_fields = ['user__username']     # with direct foreign key no error but filtering not possible directly

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    inlines = [
        DealInline,
    ]
    
    exclude = ('user',)


admin.site.unregister(User)

admin.site.register(User,UserAdmin)
admin.site.register(Product)

admin.site.register(ProductInCart)
admin.site.register(Order)

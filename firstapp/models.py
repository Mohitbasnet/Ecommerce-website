from django.db import models

# Create your models here.
from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from django.utils.translation import gettext_lazy as _ #this is used to translate string into different languages

from . managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin

from django.core.validators import RegexValidator


from multiselectfield import MultiSelectField



# class UserType(models.Model):
#     CUSTOMER = 1
#     SELLER = 2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer')
#     )
#     id = models.PositiveSmallIntegerField(choices = TYPE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()


class CustomUser(AbstractBaseUser,PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length = 255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
#   Booleanfiesds for usertype
    is_customer = models.BooleanField(default = True)
    is_seller = models.BooleanField(default = False)

    # type = (
    #     (1,'Seller'),
    #     (2, 'Customer')
    # )

    # user_type = models.IntegerField(choices = type, default = 1)
    # usertype = models.ManyToManyField(UserType)

    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"
    
    # Types = (
    #     (1, 'SELLER'),
    #     (2, 'CUSTOMER')
    # )
    # type = models.IntegerField(choices=Types, default=2)

    default_type = Types.CUSTOMER

    #type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True, max_length = 255)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        if not self.id:
            #self.type = self.default_type
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)


# For more fields we user two classes
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    address = models.CharField(max_length = 255)

class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gst = models.CharField(max_length=10)
    warehouse_location = models.CharField(max_length=1000)


class Seller(models.Model):
    user = models.OneToOneField(CustomUser , on_delete= models.CASCADE)
    gst = models.CharField(max_length = 255)
    warehouse_location = models.CharField(max_length=255)

class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.SELLER))
# Proxy Models. They do not create a seperate table
class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.CUSTOMER))


class Product(models.Model):
    product_id = models.AutoField(primary_key =True)
    product_name = models.CharField(max_length = 225)
    price = models.FloatField()

    def __str__(self):
        return self.product_name

    @classmethod
    def updateprice(cls, product_id,price):
        product = cls.objects.filter(product_id = product_id)
        product = product.first()
        product.price = price
        product.save()
        return product

    @classmethod
    def create(cls, product_name,price):
        product = Product(product_name = product_name, price = price)
        product.save()
        return product

    # @staticmethod
    # def a_static_method():
    #     """
    #       A static method has no information about instances or classes unless explicitly given, it just lives in the class (and thus its instances)
    #     """
    def __str__(self):
        return self.product_name

# Customizing cart unsing custom manager
class CartManager(models.Manager):
    def create_cart(self,user):
         cart = self.create(user = user)
        # You can perform more operations
         return cart


class Cart(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_on= models.DateTimeField()

    objects = CartManager()
class ProductInCart(models.Model):
    product_in_card_id = models.AutoField(primary_key = True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()


    class Meta:
        unique_together = (('cart','product'),)
        
class Order(models.Model):
    status_choices = (
        (1,'Not Packed'),
        (2,'Ready For Shipment'),
        (3,'Shipped'),
        (4,'Delivered')
    )
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    status = models.IntegerField(choices = status_choices, default = 1)

class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length = 255)


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=5)
    
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255,  validators=[phone_regex])
    query = models.TextField()

    # REQUIRE
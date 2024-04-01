from django.db import models

# Create your models here.


from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete = models.CASCADE)
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
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.IntegerField(choices = status_choices, default = 1)
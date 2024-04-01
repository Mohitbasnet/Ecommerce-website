from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class Product(models.Model):
    product_id = models.AutoField(primary_key =True)
    product_name = models.CharField(max_length = 225)
    price = models.FloatField()

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_on= models.DateTimeField()

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
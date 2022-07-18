from django.db import models;
from django.contrib.auth.models import User;

# Create your models here.
class Customer(models.Model):
    # ID is created by default unless you want to overwrite it
    # Setting null to True allows you to set something to blank (also avois issues when migrating)
    # Cascade means that if a user is deleted, it will also be deleted in customer
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True);
    phone = models.CharField(max_length=200, null=True);
    email = models.CharField(max_length=200, null=True);
    pfp = models.ImageField(default="logo.png", null=True, blank=True);
    date_created = models.DateTimeField(auto_now_add=True, null=True);

    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True);

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    CATEGORY = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    ]

    name = models.CharField(max_length=200, null=True);
    price = models.FloatField(null=True);
    category = models.CharField(max_length=200, null=True, choices=CATEGORY);
    description = models.CharField(max_length=200, null=True, blank=True);
    date_created = models.DateTimeField(auto_now_add=True, null=True);
    tags = models.ManyToManyField(Tag);

    def __str__(self) -> str:
        return self.name;

class Order(models.Model):
    # To be able to change from a dropdown menu you have to create a list/dict/tuple and add choices
    STATUS = [
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    ]
    # We don't remove the order if the customer is deleted, bad idea
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL);
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL);
    date_created = models.DateTimeField(auto_now_add=True, null=True);
    status = models.CharField(max_length=200, null=True, choices=STATUS);
    note = models.CharField(max_length=1000, null=True);

    def __str__(self) -> str:
        return f"{self.customer.name} | {self.product.name} | {self.status}"
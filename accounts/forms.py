from django import forms;
from django.contrib.auth.models import User;
from django.forms import ModelForm;
from django.contrib.auth.forms import UserCreationForm;
from .models import *;

class CustomerForm(ModelForm):
    class Meta():
        model = Customer;
        fields = "__all__";
        exclude = ['user'];

class OrderForm(ModelForm):
    class Meta():
        model = Order;
        # You can use '__all__'
        fields = [
            'customer',
            'product',
            'status'
        ]

class CreateUserForm(UserCreationForm):
    class Meta():
        model = User;
        fields = ['username', 'email', 'password1', 'password2'];
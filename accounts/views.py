from django.shortcuts import render, redirect;
from django.http import HttpResponse;
from django.forms import inlineformset_factory;

from django.contrib import messages;
from django.contrib.auth.forms import UserCreationForm;
from django.contrib.auth import authenticate, login, logout;
from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import Group;

from .models import *;
from .decorators import *;
from .forms import CustomerForm, OrderForm, CreateUserForm;
from .filters import OrderFilter;

# Create your views here.
@unathenticated_user
def register_page(request):
    form = CreateUserForm();

    if (request.method == "POST"):
        form = CreateUserForm(request.POST);
        if (form.is_valid()):
            user = form.save();
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account ({username}) successfully created");

            return redirect('login');

    context = {
        'form': form
    };
    return render(request, 'accounts/register.html', context);

@unathenticated_user
def login_page(request):
    if (request.method == "POST"):
        # The names are the ones from the inputs
        username = request.POST.get("username");
        password = request.POST.get("password");
        # Make sure the user is authenticated
        user = authenticate(request, username=username, password=password);
        if (user is not None):
            login(request, user);
            return redirect('home');
        else:
            messages.info(request, "Username OR password is incorrect");

    context = {};
    return render(request, 'accounts/login.html', context);

def logout_user(request):
    logout(request);
    return redirect("login");

# Decorators are executed in order
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all();
    customers = Customer.objects.all();

    total_orders = orders.count();
    delivered = orders.filter(status='Delivered').count();
    pending = orders.filter(status='Pending').count();

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    # This works because we have the one to one relation
    orders = request.user.customer.order_set.all();
    total_orders = orders.count();
    delivered = orders.filter(status='Delivered').count();
    pending = orders.filter(status='Pending').count();

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    };
    return render(request, 'accounts/user.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer;
    form = CustomerForm(instance=customer);

    if (request.method == "POST"):
        # In order to pass the files you need request.FILES
        form = CustomerForm(request.POST, request.FILES, instance=customer); 
        if (form.is_valid()):
            form.save();

    context = {
        'form': form
    };
    return render(request, 'accounts/account_settings.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    # Querys the db for all the projects
    products = Product.objects.all();
    # The name you put in here is what you need to use in the html
    return render(request, 'accounts/products.html', {'products':products});

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk);
    orders = customer.order_set.all();
    orders_count = orders.count();

    myFilter = OrderFilter(request.GET, queryset=orders);
    orders = myFilter.qs;

    context = {
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count,
        'myFilter': myFilter
    };

    return render(request, 'accounts/customer.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    # OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10);

    customer = Customer.objects.get(id=pk);

    # formset = OrderFormSet(queryset=Order.objects.none(), instance=customer);

    form = OrderForm(initial={'customer':customer});

    if (request.method == 'POST'):
        # print("Printing POST:", request.POST)
        form = OrderForm(request.POST);
        # formset = OrderFormSet(request.POST, instance=customer);
        if (form.is_valid()):
            # This saves the info into the DB
            form.save();
            return redirect(f'/customer/{pk}');

    context = {
        'form': form
    };
    return render(request, 'accounts/order_form.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk);
    # Add an instance to get the data
    form = OrderForm(instance=order);

    if (request.method == 'POST'):
        form = OrderForm(request.POST, instance=order);
        if (form.is_valid()):
            form.save();
            return redirect('/');

    context = {
        'form': form
    };
    return render(request, 'accounts/order_form.html', context);

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk);

    if (request.method == "POST"):
        order.delete();
        return redirect('/');

    context = {
        'item': order
    };
    return render(request, 'accounts/delete.html', context);
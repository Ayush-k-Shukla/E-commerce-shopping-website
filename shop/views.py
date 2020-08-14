from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.middleware.csrf import get_token
from django.views.generic import View
from math import ceil
import requests

from .models import Product, Contact, Orders, Cart
from .serialize import cartSerializer
from .forms import UserForm

    
def index(request):

    products = []
    catagory = Product.objects.values('catagory', 'id')
    cats = {item['catagory'] for item in catagory}
    for cat in cats:
        prod = Product.objects.filter(catagory = cat)
        n = len(products)
        nSlides = n//4 + ceil((n/4) - (n//4))
        products.append([prod, range(1,nSlides), nSlides])

    # Passing paras in Responce..................
    params = {'products': products}

    return render(request, 'shop/index.html', params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank' : thank})

class RegisterForm(View):
    form_user = UserForm

    # Display Blank Form
    def get(self, request):
        return render(request, 'shop/register.html')

    def post(self, request):
        form = self.form_user(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            user.set_password(password)

            user = authenticate(username=username, password=password)
            user.save()

            return redirect('shop/login')

        return render(request, 'shop/register.html')

def loginUser(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/shop')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('shop/login')
    else:
        return render(request, 'shop/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/shop')

def search(request):
    return render(request,'shop/search.html')

def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html', {'product': product[0]})

def checkout(request):

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')


def cart(request):
    u="http://127.0.0.1:8000/viewcart/"
    ln = requests.get(u).json()
    cart_items=[]
    for item in ln:
        prod_id = item['prod_id']
        qty = item['quantity']
        prod = Product.objects.get(id=int(prod_id))
        cart_items.append((prod, prod_id, qty))

    return render(request, 'shop/cart.html', {'cart':cart_items})







# Looked after by ajax..............
# def cartUpdate(request):

#     if request.method == 'GET':
#         id = request.GET['item_id']
#         item = Product.objects.get(id=id)
#         prod_id = item.id
#         user_id = 'guest'
#         quantity = 1
#         totalPrice = item.price

#         cart = Cart(prod_id=prod_id, user_id=user_id, quantity=quantity, totalPrice=totalPrice)
#         cart.save()

#         print('i am saved')
#         return redirect('/shop')

#     else:
#         return HttpResponse("<h1>Request is not POST</h1>")


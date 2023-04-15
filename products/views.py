from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Offer, Order, Categorie, Comment
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}
    # products = Product.objects.all()
    categories = Categorie.objects.all()
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        if categorie_id == "10":
            print("Albert")
            products = Product.objects.all()
        else:
            products = Product.get_all_products_by_categorieid(categorie_id)
    else:
        products = Product.objects.all()
    data = {}
    data['products'] = products
    data['categories'] = categories
    # return HttpResponse('Hello, Welcome to the project')
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    if product is not None:
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
    return render(request, 'index.html', data)


def cart(request):
    if request.method == 'POST':
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})
    else:
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})


def thank_you(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user_id = request.session.get('user_id')
        carts = request.session.get('cart')
        products = Product.get_products_by_id(list(carts.keys()))
        print(address, phone, user_id, carts, products)

        if len(phone) == 11:
            if phone[0] in "01":
                for product in products:
                    order = Order(user=User(id=user_id), product=product, price=product.price,
                                  quantity=carts.get(str(product.id)), address=address, phone=phone)
                    order.place_order()
                request.session['cart'] = {}
                return render(request, 'Thank you.html')
            else:
                messages.error(request, 'Invalid Phone number')
                return redirect('/products/cart')
        else:
            messages.error(request, 'Phone no. should have 11 digits')
            return redirect('/products/cart')

    else:
        return redirect('/')

from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime

def view_index(request):
    return render(request,'view_index.html')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'price','stock']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Enter Product Name:',
            'image': 'Select an Image: ',
            'category': 'Select Category: ',
            'price': 'Enter a price: ',
            'stock': 'Enter available Quantity',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.Textarea(attrs={'class': 'form-control'}),
        }

def addProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/products/')
    else:
        form = ProductForm()

    context = {
        "form":form
    }

    return render(request, 'addProduct.html', context)

def add_comment(request, pk=10):

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(Product, commenter_name=name, comment_body=body, date_added=datetime.now())
            c.save()
            return redirect('http://127.0.0.1:8000/product/10/add-comment')
        else:
            print('form is invalid')
    else:
        form = CommentForm()

    context = {
        'form': form
    }

    return render(request, 'add_comment.html', context)


def delete_comment(request, pk):
    comment = Comment.objects.filter(product=pk).last()
    product_id = comment.product.id
    comment.delete()
    return redirect(reverse('product', args=[product_id]))


def delete_comment(request, pk):
    comment = Comment.objects.filter(product=pk).last()
    product_id = comment.product.id
    comment.delete()
    return redirect(reverse('product', args=[product_id]))

def updateProduct(request,pk):
    product = Product.objects.get(id=pk)

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/products/')

    context = {
        "form":form
    }
    return render(request, 'updateProduct.html', context)

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('http://127.0.0.1:8000/products/')
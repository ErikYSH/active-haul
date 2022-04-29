from re import template
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import LoginForm, ProductCreationForm, ProductUpdateForm, SignUpForm
from .models import Product, OrderItem, Orders
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

def home(request):
    # product = Product.objects.all()
    product = "hi"
    user = request.user
    context = {
        'product':product,
    }
    return render(request, 'home.html', {'context': context})


class Products_Index(TemplateView):
    template_name = 'products.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user=user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Womens(TemplateView):
    template_name = 'product_womens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Mens(TemplateView):
    template_name = 'product_mens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Accessories(TemplateView):
    template_name = 'product_accessories.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        print(title)
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

def product_create(request):
    product = Product.objects.all()
    user = request.user
    form_class = ProductCreationForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return HttpResponseRedirect ('/')
    else:
        form = form_class
    context = {
        'form':form
    }
    return render (request, 'product_create.html', context)    

# def product_show(request, slug):
#     # products = get_object_or_404(Product, id=id) 
#     product = Product.objects.get(slug=slug)
#     return render(request, 'product_show.html', {'product':product})

class Product_Show(DetailView):
    model = Product
    template_name = "product_show.html"

class Product_Update(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = '/products'
    # def get_success_url(self):
        # return reverse('product_show', kwargs={'id': self.object.id})
        # return HttpResponseRedirect('/products') 

class Product_Delete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = '/products'


#### AUTHENTICATION
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            e = form.cleaned_data.get('email')
            p = form.cleaned_data.get('password')
            user = authenticate(email = e, password = p)
            if user is not None: 
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else: 
                    print('The account has been disabled')
                    return HttpResponseRedirect('/login')
        else:
            messages.sucess(request, 'The username and/or password is incorrect')
            return HttpResponseRedirect('/login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

def signup_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print('Hi', user.username)
            # return HttpResponseRedirect('/user/'+str(user.username))
            return HttpResponseRedirect('/')
        else:
            return render(request, 'signup.html', {'form':form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.create(product=product)
    order_queryset = Orders.objects.filter(user=request.user, ordered= False)
    if order_queryset.exists():
        order = order_queryset[0]
        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Orders.objects.create(user=request.user, ordered_date = ordered_date)
        order.product.add(order_item)
    return redirect('/product', slug=slug)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, ordered=False)
        items = order.product.all()
    else:
        items = []
    context = {'items':items}
    return render(request, 'cart_view.html', context)
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import LoginForm, ProductCreationForm, ProductUpdateForm, SignUpForm
from .models import Account, Product, OrderItem, Orders
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

User = get_user_model()

def home(request):
    products = Product.objects.all()
    print(products)
    context = {
        'products':products,
    }
    return render(request, 'home.html', context)


class Products_Index(TemplateView):
    template_name = 'products.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user=user.id)
        if title != None:
            context['products'] = Product.objects.filter(title__icontains=title)
        else:
            context['products'] = Product.objects.all()
        return context

# @method_decorator(login_required, name='dispatch')
class Products_Womens(TemplateView):
    template_name = 'product_womens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        # products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = Product.objects.filter(title__icontains=title)
        else:
            context['products'] = Product.objects.all()
        return context

class Products_Mens(TemplateView):
    template_name = 'product_mens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = Product.objects.filter(title__icontains=title)
        else:
            context['products'] = Product.objects.all()
        return context

class Products_Accessories(TemplateView):
    template_name = 'product_accessories.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        print(title)
        user = self.request.user
        if title != None:
            context['products'] = Product.objects.filter(title__icontains=title)
        else:
            context['products'] = Product.objects.all()
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
    products = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(product=products)
    order_queryset = Orders.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        if order.product.filter(product__slug=products.slug).exists():
            order_item.quantity += 1
            order_item.save()
            print(order_item)
        else:
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Orders.objects.create(user=request.user, ordered_date = ordered_date)
        order.product.add(order_item)
    return redirect('product_show', slug=slug)
    # return HttpResponseRedirect('/product')

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(user=user, ordered=False)
        items = order.product.all()
    else:
        items = []
    context = {'items':items}
    return render(request, 'cart_view.html', context)
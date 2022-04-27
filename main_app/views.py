from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import ProductCreationForm, ProductUpdateForm
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
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
        print(title)
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
        print(title)
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

def product_show(request, product_id):
    # products = get_object_or_404(Product, id=id) 
    product = Product.objects.get(id=product_id)
    return render(request, 'product_show.html', {'product':product})

class Product_Update(UpdateView):
    template_name = 'product_update.html'
    model = Product
    print(Product.id)
    form_class = ProductUpdateForm
    success_url = '/products'
    # def get_success_url(self):
        # return reverse('product_show', kwargs={'id': self.object.id})
        # return HttpResponseRedirect('/products') 
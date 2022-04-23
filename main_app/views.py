from django.shortcuts import render
from .forms import ProductCreationForm
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def home(request):
    # product = Product.objects.all()
    product = "hi"
    user = request.user
    context = {
        'product':product,
    }
    return render(request, 'home.html', {'context': context})


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
            return HttpResponseRedirect ('/product')
    else:
        form = form_class
    context = {
        'form':form
    }
    return render (request, 'product_create.html', context)    





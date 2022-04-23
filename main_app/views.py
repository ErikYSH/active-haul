from django.shortcuts import render
from .forms import ProductCreationForm
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView

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





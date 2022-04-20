from django.shortcuts import render


# Create your views here.

def home(request):
    context = "Home page"
    return render(request, 'home.html', {'context': context})



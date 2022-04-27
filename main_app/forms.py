from .models import Product
from django import forms


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ("title", 'description','main_category','category','size','color','image', 'price', 'conditions', 'user')
       
class ProductUpdateForm(forms.ModelForm):
     class Meta:
        model = Product 
        fields = ("title", 'description','main_category','category','size','color','image', 'price', 'conditions', 'user')
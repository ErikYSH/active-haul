from .models import Product, Account
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm 
from django import forms


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ("title", 'description','main_category','category','size','color','image', 'price', 'conditions', 'user')
       
class ProductUpdateForm(forms.ModelForm):
     class Meta:
        model = Product 
        fields = ("title", 'description','main_category','category','size','color','image', 'price', 'conditions', 'user')

    
class LoginForm(forms.ModelForm):
    password = forms.CharField(label= 'Password', widget= forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ['email', 'password']
    
    def clean(self):
        if self.is_valid:
            email = self.cleaned_data.get('email').lower()
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email or Password incorrect")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = Account.get(email=email)
        except Exception as e: 
            return email
        raise forms.ValidationError(f"Email {email} is already in use")
from audioop import reverse
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
# Create your models here.


# Create a new user
# Create a superuser

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email: 
                raise ValueError('Users must have an email address')
        if not username: 
                raise ValueError('Users must have an username')
        user = self.model(
            email=self.normalize_email(email), # help remove the problem of user input lowercase
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser (self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), # help remove the problem of user input lowercase
            username = username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'profile_img/{self.pk}/{"profile_img.png"}'

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(max_length=30 , unique=True)
    bio = models.TextField(max_length=350,)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to='images/' , null=True, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

MAIN_CATEGORY = {
    ('Womens', 'Womens'),
    ('Mens', 'Mens'),
    ('Accessories', 'Accessories'),
}

CATEGORY = {
    ('Bottoms', 'Bottoms'),
    ('Joggers', 'Joggers'),
    ('Leggings', 'Leggings'),
    ('Shorts', 'Shorts'),
    ('T-shirts & Tops', 'T-shirt & Tops'),
    ('Hoddies & Jackets', 'Hoddies & Jackets'),
    ('Crop Tops', 'Crop Tops'),
    ('Sports Bras', 'Sports Bras'),
    ('Tank Tops', 'Tank Tops'),
    ('Gym Bags', 'Gym Bags'),
    ('Headwears', 'Headwears'),
    ('Equipments', 'Equipments'),
}

CONDITIONS ={
    ('New', 'New'),
    ('Used - Like New', 'Used - Like New'),
    ('Used - Good', 'Used - Good'),
    ('Used - Fair', 'Used - Fair'),
}


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    main_category = models.CharField(max_length=30, choices=MAIN_CATEGORY)
    category = models.CharField(max_length=50, choices=CATEGORY)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/' , null=True, blank=True)
    price = models.IntegerField()
    conditions = models.CharField(max_length=20, choices=CONDITIONS)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def add_to_cart_url(self):
        return reverse('/add_to_cart', kwargs={
            'product_id':self.product_id
        })



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add =True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 


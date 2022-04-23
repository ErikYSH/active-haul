from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.home, name='home'),
    path('products/create', views.product_create, name="product_create"),

]
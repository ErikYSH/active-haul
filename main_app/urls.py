from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.Products_Index.as_view(), name='products_index'),
    path('products/create', views.product_create, name="product_create"),
    # path('products/<int:pk>', views.product_show, name='product_show'),

]
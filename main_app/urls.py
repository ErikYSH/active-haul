from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.Products_Index.as_view(), name='products_index'),
    path('products/womens', views.Products_Womens.as_view(), name='products_womens'),
    path('products/mens', views.Products_Mens.as_view(), name='products_mens'),
    path('products/accessories', views.Products_Accessories.as_view(), name='products_accessories'),
    path('products/create', views.product_create, name="product_create"),
    path('products/<int:product_id>', views.product_show, name='product_show'),
    path('products/<int:pk>/update', views.Product_Update.as_view(), name='product_update'),
    path('products/<int:pk>/delete', views.Product_Delete.as_view(), name='product_delete'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('products/cart', views.cart, name='cart'),
]

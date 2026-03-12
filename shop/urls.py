from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:tracking_code>/', views.order_confirmation, name='order_confirmation'),
    path('order-status/', views.order_status, name='order_status'),
    path('cart-count/', views.cart_count, name='cart_count'),
]

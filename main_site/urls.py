from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('certifications/', views.certifications, name='certifications'),
    path('where-to-buy/', views.where_to_buy, name='where_to_buy'),
    path('contact/', views.contact, name='contact'),
]

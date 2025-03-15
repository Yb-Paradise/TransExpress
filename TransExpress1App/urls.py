from django.contrib import admin
from django.urls import path

from TransExpress1App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('starter/', views.starter, name='starter'),
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('quote/', views.quote, name='quote'),
    path('price/', views.price, name='price'),
    path('contacts/', views.contacts, name='contacts'),
    path('editquote/<int:id>', views.editquote, name= 'edit-delivery-details'),
    path('deletequote/<int:id>', views.deletequote, name='delete-delivery-details'),
    path('details/', views.details, name='details'),
    path('show/', views.showquote, name='show'),
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    #Mpesa API

    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),




]
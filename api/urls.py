import imp
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'), # Root
    path('import/', views.importData , name='home'),  # import API to import data from salesforce. 
    path('opportunities/', views.opportunities , name='home'), # An API to view all Opportunties
    path('accounts/', views.accounts , name='home'), # An API to view all Accounts
    path('users/', views.users , name='home'), # An API to view all Users 
    
]

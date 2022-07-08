import imp
from django.contrib import admin
from django.urls import path,re_path
from . import views
urlpatterns = [
    path('', views.home , name='home'), # Root
    path('import/', views.importData , name='home'),  # import API to import data from salesforce. 


    # An API to view all Opportunties
    re_path(r'^opportunities/$', views.opportunities , name='home'),
    re_path(r'^opportunities/pageNo=(?P<pageNo>\w+)', views.opportunities , name='home'),
   
    # An API to view all Accounts
    re_path(r'^accounts/$', views.accounts , name='home'),
    re_path(r'^accounts/pageNo=(?P<pageNo>\w+)', views.accounts , name='home')

    ,
    # An API to view all Users 
    re_path(r'^users/$', views.users , name='home'), 
    re_path(r'^users/pageNo=(?P<pageNo>\w+)', views.users , name='home'), 
    
]

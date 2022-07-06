from curses.ascii import US
from django.contrib import admin
from .models import Account, Userm, Opportunity
# Register your models here.

admin.site.register( {Account, Userm, Opportunity})
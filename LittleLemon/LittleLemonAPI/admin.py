from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
# Register your models here.

admin.site.register([Category,
                     MenuItem, 
                     Cart, 
                     Order, 
                     OrderItem])
from rest_framework import serializers 
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.contrib.auth.models import User 
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'title': {
            'validators': [
                UniqueValidator(queryset=Category.objects.all())
            ]
            }
        }
        

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        extra_kwargs = {
            'price': {'min_value': 0.01},
            'title': {
            'validators': [
                UniqueValidator(queryset=MenuItem.objects.all())
            ]
            }
        }
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Order.objects.all(),
                fields=['user', 'date'],
                message='You already have an order for this date.'
            )
        ]
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['price']
        extra_kwargs = {
            'quantity': {'min_value': 1},
            'user': {'read_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=['user', 'menuitems'],
                message='This item is already in your cart.'
            )
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['price']
        extra_kwargs = {
            'quantity': {'min_value': 1},
            'order': {'read_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=OrderItem.objects.all(),
                fields=['order', 'menuitem'],
                message='This item is already in your order.'
            )
        ]
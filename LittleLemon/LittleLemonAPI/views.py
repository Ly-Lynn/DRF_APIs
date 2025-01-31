from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from djoser.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from .filters import OrderFilter
from .permissions import MenuItemPermission, OrderPermission, IsDelivery, IsManager, CartPermission

from .models import MenuItem, Order, OrderItem, Cart, Category
from .serializers import MenuItemSerializer, OrderSerializer, CartSerializer, OrderItemSerializer, CategorySerializer

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'per_page' 
    max_page_size = 100

# User group management API views
class ManagerManagement(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    filterset_fields = ['username', Group]
    search_fields = ['username']
    ordering_fields = ['username']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(groups__name="Managers")
    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
            manager_group, _ = Group.objects.get_or_create(name="Managers")
            user.groups.add(manager_group)
            return Response({"message": f"{user.username} is added into Managers Group."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
class ManagerDelete(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            manager_group = Group.objects.get(name="Managers")
            user.groups.remove(manager_group)
            return Response({"message": f"{user.username} is deleted out of Managers Group."}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Managers Group does not exist"}, status=status.HTTP_404_NOT_FOUND)
class DeliveryCrewManagement(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    search_fields = ['username']
    ordering_fields = ['username']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(groups__name="Delivery crew")
    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
            delivery_crew_group, _ = Group.objects.get_or_create(name="Delivery crew")
            user.groups.add(delivery_crew_group)
            return Response({"message": f"{user.username} is added into Delivery Crew Group."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
class DeliveryCrewDelete(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            delivery_crew_group = Group.objects.get(name="Delivery crew")
            user.groups.remove(delivery_crew_group)
            return Response({"message": f"{user.username} is deleted out of Delivery Crew Group."}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Delivery Crew Group does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Category API views
class CategoryViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [MenuItemPermission]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']
    pagination_class = CustomPageNumberPagination
# Menu Item API views
class MenuItemViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemPermission]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'price']
    ordering_fields = ['price', 'title']
    pagination_class = CustomPageNumberPagination

# Cart API views
class CartViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CartPermission]
    filterset_fields = ['user', 'menuitems']
    search_fields = ['user', 'menuitems']
    ordering_fields = ['user', 'menuitems']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    @action(detail=False, methods=["DELETE"], url_path="clear", url_name="clear")
    def clear(self, request, *args, **kwargs):
        print("Request method:", request.method)
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_items.delete()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        user = request.user
        menuitem_id = request.data.get("menuitem_id")
        quantity = request.data.get("quantity")
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
            total_price = quantity * menuitem.price
            check_exists = Cart.objects.filter(user=user, menuitems=menuitem).exists()
            if check_exists:
                cart_item = Cart.objects.get(user=user, menuitems=menuitem)
                cart_item.quantity += quantity
                cart_item.price += total_price
                cart_item.save()
                return Response({"message": f"Item added MORE to cart\n{cart_item}"}, status=status.HTTP_201_CREATED)
            cart_item, _ = Cart.objects.get_or_create(user=user, 
                                    menuitems=menuitem, quantity=quantity, unit_price=menuitem.price, price=total_price)
            return Response({"message": f"Item added to cart\n{cart_item}"}, status=status.HTTP_201_CREATED)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Order API views
class OrderViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]
    filterset_class = OrderFilter
    search_fields = ['user', 'delivery_crew', 'status']
    ordering_fields = ['user', 'delivery_crew', 'status']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Managers").exists():
            return Order.objects.all()
        if user.groups.filter(name="Delivery crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        order = self.get_object()   
        if order.user != user and order.delivery_crew != user and not user.groups.filter(name="Managers").exists():
            return Response({"error": "You are not allowed to view this order"}, status=status.HTTP_403_FORBIDDEN)
        order_items = OrderItem.objects.filter(order=order)
        order_data = OrderSerializer(order).data
        order_data["order_items"] = OrderItemSerializer(order_items, many=True).data
        return Response({"order": order_data}, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)
        if not cart.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        total_price = sum(item.price for item in cart)

        new_order = Order.objects.create(user=user, total=total_price, date=now())
        order_items = []
        for cart_item in cart:
            order_items.append(OrderItem(order=new_order,       
                                menuitem=cart_item.menuitems, quantity=cart_item.quantity, unit_price=cart_item.unit_price, price=cart_item.price))
        OrderItem.objects.bulk_create(order_items)
        cart.delete()
        return Response({"message": f"Order created\n{new_order}"}, status=status.HTTP_201_CREATED)
    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        if user.groups.filter(name="Managers").exists():
            order.status = request.data.get("status") or order.status
            delivery_crew = request.data.get("delivery_crew") 
            if delivery_crew:
                order.delivery_crew = User.objects.get(id=delivery_crew)
            order.save()
            return Response({"message": f"Order status updated\n{order} by manager {user.id}"}, status=status.HTTP_200_OK)
        if user.groups.filter(name="Delivery crew").exists():
            if any(field for field in request.data if field != "status"):
                return Response({"error": "Delivery crew can only update status"}, status=status.HTTP_403_FORBIDDEN)
            order.status = request.data.get("status")
            order.save()
            return Response({"message": f"Order status updated\n{order} by delivery crew {user.id}"}, status=status.HTTP_200_OK)

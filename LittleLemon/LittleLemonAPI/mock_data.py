from django.utils import timezone
from django.contrib.auth.models import User
from LittleLemonAPI.models import Category, MenuItem, Cart, Order, OrderItem  

customer1 = User.objects.get_or_create(username="lynn_customer")
customer2 = User.objects.get_or_create(username="lynn_customer2")
delivery_crew = User.objects.get_or_create(username="lynn_delivery")

categories = [
    Category.objects.create(slug="appetizers", title="Appetizers"),
    Category.objects.create(slug="main-course", title="Main Course"),
    Category.objects.create(slug="desserts", title="Desserts"),
    Category.objects.create(slug="beverages", title="Beverages"),
    Category.objects.create(slug="snacks", title="Snacks"),
]

menu_items = [
    MenuItem.objects.create(title="Spring Rolls", price=5.99, featured=True, category=categories[0]),
    MenuItem.objects.create(title="Grilled Chicken", price=12.99, featured=False, category=categories[1]),
    MenuItem.objects.create(title="Chocolate Cake", price=6.50, featured=True, category=categories[2]),
    MenuItem.objects.create(title="Orange Juice", price=3.99, featured=False, category=categories[3]),
    MenuItem.objects.create(title="French Fries", price=4.50, featured=True, category=categories[4]),
]

carts = [
    Cart.objects.create(user=customer1[0], menuitems=menu_items[0], quantity=2, unit_price=5.99, price=11.98),
    Cart.objects.create(user=customer1[0], menuitems=menu_items[1], quantity=1, unit_price=12.99, price=12.99),
    Cart.objects.create(user=customer2[0], menuitems=menu_items[2], quantity=3, unit_price=6.50, price=19.50),
    Cart.objects.create(user=customer2[0], menuitems=menu_items[3], quantity=2, unit_price=3.99, price=7.98),
    Cart.objects.create(user=customer2[0], menuitems=menu_items[4], quantity=4, unit_price=4.50, price=18.00),
]

orders = [
    Order.objects.create(user=customer1[0], delivery_crew=delivery_crew[0], status=True, total=30.00, date=timezone.now()),
    Order.objects.create(user=customer2[0], delivery_crew=delivery_crew[0], status=False, total=20.00, date=timezone.now()),
    Order.objects.create(user=customer1[0], delivery_crew=None, status=True, total=15.00, date=timezone.now()),
    Order.objects.create(user=customer2[0], delivery_crew=None, status=False, total=25.00, date=timezone.now()),
    Order.objects.create(user=customer1[0], delivery_crew=delivery_crew[0], status=True, total=40.00, date=timezone.now()),
]

order_items = [
    OrderItem.objects.create(order=orders[0], menuitem=menu_items[0], quantity=2, unit_price=5.99, price=11.98),
    OrderItem.objects.create(order=orders[1], menuitem=menu_items[1], quantity=1, unit_price=12.99, price=12.99),
    OrderItem.objects.create(order=orders[2], menuitem=menu_items[2], quantity=3, unit_price=6.50, price=19.50),
    OrderItem.objects.create(order=orders[3], menuitem=menu_items[3], quantity=2, unit_price=3.99, price=7.98),
    OrderItem.objects.create(order=orders[4], menuitem=menu_items[4], quantity=4, unit_price=4.50, price=18.00),
]

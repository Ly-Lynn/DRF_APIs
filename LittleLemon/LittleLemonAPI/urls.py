from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, OrderViewSet, ManagerManagement, ManagerDelete, DeliveryCrewManagement, DeliveryCrewDelete, CartViewSet

router = DefaultRouter()
router.register(r"menu-items", MenuItemViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"cart/menu-items", CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    # User group management endpoints# User group management endpoints
    path('groups/manager/users/', ManagerManagement.as_view(), name='manager-management'),
    path('groups/manager/users/<int:pk>/', ManagerDelete.as_view(), name='manager-delete'),
    path('groups/delivery-crew/users/', DeliveryCrewManagement.as_view(), name='delivery-crew-management'),
    path('groups/delivery-crew/users/<int:pk>/', DeliveryCrewDelete.as_view(), name='delivery-crew-delete'),
    
    # djoser
    
    path('auth/', include('djoser.urls')),
    # path('auth/', include("djoser.urls.jwt")),
    path('auth/', include("djoser.urls.authtoken")),
]
from django.urls import path
from . import views
from .views import MenuItemsView, SingleMenuItemView, BookingViewSet


urlpatterns = [
    path('menu-items/', MenuItemsView.as_view()),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view()),
   
]
 
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Booking, MenuItem
from .serializers import (
    BookingSerializer,
    MenuSerializer,
    MenuItemSerializer,
    UserSerializer
)
from datetime import datetime
from django.core import serializers
from .forms import BookingForm
from django.http import HttpResponse

def sayHello(request):
    return HttpResponse('Hello World')


def home(request):
    return render(request, 'index.html', {})


# ---------------------------
#   BOOKING API (Correct)
# ---------------------------
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


# ---------------------------
#   MENU ITEMS API (Correct)
# ---------------------------
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# ---------------------------
#   USER VIEWSET
# ---------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---------------------------
#   HTML VIEWS
# ---------------------------
def about(request):
    return render(request, 'about.html')


def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json})


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'book.html', {'form': form})

def menu(request):
    menu_data = MenuItem.objects.all()
    return render(request, 'menu.html', {"menu": menu_data})

def display_menu_item(request, pk=None):
    menu_item = MenuItem.objects.get(pk=pk)
    return render(request, 'menu_item.html', {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if request.method == "POST":
            form = BookingForm(request.POST)
        if form.is_valid():      # validation happens here
            form.save()

        # Validate guests
        guests = data.get('no_of_guests')
        if guests in (None, ''):
            return HttpResponse('{"error": "no_of_guests required"}', content_type='application/json')

        try:
            guests = int(guests)
        except ValueError:
            return HttpResponse('{"error": "no_of_guests must be a number"}', content_type='application/json')

        # Check for existing booking
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()

        if exist:
            return HttpResponse('{"error":1}', content_type='application/json')

        # Create booking
        Booking.objects.create(
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
            no_of_guests=guests
        )

        return HttpResponse('{"success":1}', content_type='application/json')

    # GET
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.today().date()

    bookings = Booking.objects.filter(reservation_date=date).order_by('reservation_slot')
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

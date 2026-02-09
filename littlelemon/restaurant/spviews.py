from django.shortcuts import HttpResponse, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Menu
from .serializers import bookingSerializer, menuSerializer


# Create your views here.
def sayHello(request):
    return HttpResponse('Hello World')

def index(request):
    return render(request, 'index.html', {})

class bookingview(APIView):

    def get(self,request):
        items = Booking.objects.all()
        serializer = bookingSerializer(items, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = bookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.is_valid()
            return Response({"status": "success", "data": serializer.data})

class menuview(APIView):
    def get(self,request):
        items = Menu.objects.all()
        serializer = menuSerializer(items, many = True)
        return Response(serializer.data)

    def post(self, request):
        items = Menu.objects.all()
        serializer = menuSerializer(data=request.data)

        if serializer.is_valid():
            serializer.is_valid()
            return Response({"status": "success", "data": serializer.data})
from django.shortcuts import HttpResponse, render

# Create your views here.
def sayHello(request):
    return HttpResponse('Hello World')

def index(request):
    return render(request, 'index.html', {})
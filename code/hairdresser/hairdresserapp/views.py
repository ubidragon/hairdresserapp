from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    
    return render(request, "hairdresserapp/home.html")

def servicios(request):
    
    return render(request, "hairdresserapp/servicios.html")

def contacto(request):
    
    return render(request, "hairdresserapp/contacto.html")
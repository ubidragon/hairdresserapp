from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    
    return render(request, "hairdresserapp_gestionCitas/home.html")

def servicios(request):
    
    return render(request, "hairdresserapp_gestionCitas/servicios.html")

def citas(request):
    
    return render(request, "hairdresserapp_gestionCitas/citas.html")
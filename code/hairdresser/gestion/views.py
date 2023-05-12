from django.shortcuts import render, redirect
from django.http import HttpResponse,  HttpRequest

# Create your views here.


def home(request):
    
    return render(request, "gestion/home.html")

def servicios(request):
    
    return render(request, "gestion/servicios.html")

def citas(request):
    
    if request.GET.get("action") == "crearCita":
        return redirect("Gestion")
    return render(request, "gestion/citas.html")

def ofertas(request):
    
    return render(request, "gestion/ofertas.html")

def usuarios(request):
        
    return render(request, "gestion/usuarios.html")
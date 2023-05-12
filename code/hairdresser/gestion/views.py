from django.shortcuts import render, redirect
from django.http import HttpResponse,  HttpRequest
from .models import *
# Create your views here.


def home(request):
    
    return render(request, "gestion/home.html")

def servicios(request):
    servicios=Servicio.objects.all() 
    return render(request, "gestion/servicios.html", {"servicios":servicios})

def citas(request):
    citas=Cita.objects.all()
    if request.GET.get("action") == "crearCita":
        return redirect("Gestion")
    return render(request, "gestion/citas.html", {"citas":citas})

def ofertas(request):
    ofertas=Oferta.objects.all()
    return render(request, "gestion/ofertas.html", {"ofertas":ofertas})

def usuarios(request):
    usuarios=Usuario.objects.all() 
    return render(request, "gestion/usuarios.html", {"usuarios":usuarios})
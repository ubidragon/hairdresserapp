from django.shortcuts import render, redirect
from .forms import inicioSesion, registro
# Create your views here.

def login(request):
    
    return render(request, "acceso/login.html", {'formularioInicio':inicioSesion})

def logout(request):
    
    return redirect("/")

def signUp(request):
    
    return render(request, "acceso/signup.html", {'formularioRegistro':registro})
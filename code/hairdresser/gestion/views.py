from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    
    return render(request, "gestion/home.html")

def servicios(request):
    
    return render(request, "gestion/servicios.html")

def citas(request):
    
    return render(request, "gestion/citas.html")
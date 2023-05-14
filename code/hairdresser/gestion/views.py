from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,  HttpRequest
from django.views.generic import FormView
from .models import *
from .forms import crearServicioForm
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

def obtener_objeto_por_id(Modelo, id):
		try:
				objeto = Modelo.objects.get(id=id)
				return objeto
		except Modelo.DoesNotExist:
				return None

def crear(request):
		referer = request.POST.get('referer')
		if referer is not None:
			if "servicios/crear" in referer :
				nuevoServicio = crearServicioForm(request.POST)
				if nuevoServicio.is_valid() :
					ubicacion_nombre = nuevoServicio.cleaned_data['ubicacion']
					ubicacionObject = Ubicacion.objects.get(nombre=ubicacion_nombre)
			
					servicioObject = Servicio(nombre = nuevoServicio.cleaned_data['servicio'], precio = nuevoServicio.cleaned_data['precio'], duracion = nuevoServicio.cleaned_data['duracion'], ubicacion = ubicacionObject, descripcion = nuevoServicio.cleaned_data['descripcion'])
			
					if nuevoServicio.cleaned_data['oferta'] is not None:
						oferta_nombre = nuevoServicio.cleaned_data['oferta']
						servicioObject.oferta = Oferta.objects.get(nombre=oferta_nombre)

					servicioObject.save()
			return redirect("Servicios")
 
		# elemento = get_object_or_404(Servicio, pk=pk)
		if len(request.GET) > 0:
			elementoDb = obtener_objeto_por_id(Servicio, request.GET.get('id'))
			
			# elemento.initial["ubicacion"] = elementoDb.ubicacion.id
			initial_data = {'ubicacion':  elementoDb.ubicacion.nombre,
                   'oferta':  elementoDb.servicio_oferta_set.first().oferta_id
                   }
			elemento = crearServicioForm(instance=elementoDb,initial=initial_data)

			# elemento.get_initial(elementoDb.ubicacion.nombre)
			# elemento(initial={'ubicacion':  elementoDb.ubicacion.nombre})
	 		# elemento.initial.set
			return render(request, "gestion/snippets/creacion.html", {"data":[elemento]})
	 
	
		return render(request, "gestion/snippets/creacion.html", {"data":crearServicioForm})

# def crearServicio(request):
#     servicios=Servicio.objects.all()
#     return redirect("Crear")
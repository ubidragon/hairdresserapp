from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,  HttpRequest
from django.views.generic import FormView
from .models import *
from .forms import *
# Create your views here.


def home(request):
	
	return render(request, "gestion/home.html")

def servicios(request):
	servicios=Servicio.objects.all()
	return render(request, "gestion/servicios.html", {
     	"servicios":servicios,
      	"url_modificar": reverse('ServiciosModificar')
    	})

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

def accionesServicio(request):
		referer = request.POST.get('referer')
		if referer is not None:
			if "servicios/crear" in referer :
				nuevoServicio = crearServicioForm(request.POST)
				if nuevoServicio.is_valid() :
					ubicacion_nombre = nuevoServicio.cleaned_data['ubicacion']
					ubicacionObject = Ubicacion.objects.get(nombre=ubicacion_nombre)
			
					servicioObject = Servicio(nombre = nuevoServicio.cleaned_data['nombre'], precio = nuevoServicio.cleaned_data['precio'], duracion = nuevoServicio.cleaned_data['duracion'], ubicacion = ubicacionObject, descripcion = nuevoServicio.cleaned_data['descripcion'], activo = nuevoServicio.cleaned_data['activo'])
			
					if nuevoServicio.cleaned_data['oferta'] is not None:
						oferta_id = nuevoServicio.cleaned_data['oferta'].id
						servicioObject.oferta = Oferta.objects.get(id=oferta_id)

					servicioObject.save()
			return redirect("Servicios")
 
		if len(request.GET) > 0:
      
			ofertaData=""
			ubicacionData=""      
			servicioDb = obtener_objeto_por_id(Servicio, request.GET.get('id'))
   
			if servicioDb.oferta.first() is not None:
				ofertaDb= obtener_objeto_por_id(Oferta, servicioDb.oferta.first().id)
				ofertaData=ofertaDb.nombre
      
			if  servicioDb.ubicacion.nombre is not None:
				ubicacionData= servicioDb.ubicacion.nombre
   
   
			initial_data = {'ubicacion': ubicacionData,
                   'oferta': ofertaData,
                   'activo': servicioDb.activo
                   }
			elemento = modificarServicioForm(instance=servicioDb,initial=initial_data)

			return render(request, "gestion/snippets/creacion.html", {
       			"accion":"modificar",
				"data":[elemento],
				"url_destino": reverse('ServiciosModificar'),
				"url_listado": reverse('Servicios'),
				"tipo" : "servicio"
    		})
	 
	
		return render(request, "gestion/snippets/creacion.html", {
      		"accion":"crear",
        	"data":crearServicioForm,
         	"url_destino": reverse('ServiciosCrear'),
			"url_listado": reverse('Servicios'),
			"tipo" : "servicio"
          	})

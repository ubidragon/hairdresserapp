from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,  HttpRequest
from django.views.generic import FormView
from .models import *
from .forms import *
from .utils_gestion import *
from .servicio import *

# Create your views here.
@login_required(login_url='acceso/login.html')
def home(request):
	return render(request, "gestion/home.html")
@login_required(login_url='acceso/login.html')
def servicios(request):
	servicios=Servicio.objects.all()
	return render(request, "gestion/servicios.html", {
     	"servicios":servicios,
      	"url_modificar": reverse('ServiciosModificar')
    	})
@login_required(login_url='acceso/login.html')
def citas(request):
	citas=Cita.objects.all()
	if request.GET.get("action") == "crearCita":
		return redirect("Gestion")
	return render(request, "gestion/citas.html", {
		"citas":citas,
		"url_modificar": reverse('CitasModificar')
  	})
@login_required(login_url='acceso/login.html')
def ofertas(request):
	ofertas=Oferta.objects.all()
	return render(request, "gestion/ofertas.html", {
		"ofertas":ofertas,
  		"url_modificar": reverse('OfertasModificar')
    })
@login_required(login_url='acceso/login.html')
def usuarios(request):
	usuarios=Usuario.objects.all() 
	return render(request, "gestion/usuarios.html", {
		"usuarios":usuarios,
		"url_modificar": reverse('UsuariosModificar')
  	})
@login_required(login_url='acceso/login.html')
def accionesOferta(request):
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearOfertaForm,
		"url_destino": reverse('OfertasCrear'),
		"url_listado": reverse('Ofertas'),
		"tipo" : "oferta"
		})

@login_required(login_url='acceso/login.html')
def accionesCita(request):
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearCitaForm,
		"url_destino": reverse('CitasCrear'),
		"url_listado": reverse('Citas'),
		"tipo" : "cita"
		})
@login_required(login_url='acceso/login.html')
def accionesUsuario(request):
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearUsuarioForm,
		"url_destino": reverse('UsuariosCrear'),
		"url_listado": reverse('Usuarios'),
		"tipo" : "usuario"
		})

@login_required(login_url='acceso/login.html')
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

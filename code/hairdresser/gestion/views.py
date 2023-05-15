from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from .forms import *
from .utils_gestion import *

# Create your views here.
@login_required(login_url='/acceso/login.html')
def home(request):
	user = request.user
	return render(request, "gestion/home.html", {"rol": user.role.nombre})

@login_required(login_url='/acceso/login.html')
def servicios(request):
	user = request.user
	servicios=Servicio.objects.all()
	return render(request, "gestion/servicios.html", {
     	"servicios":servicios,
      	"url_modificar": reverse('ServiciosModificar'),
    	"rol": user.role.nombre})
 
@login_required(login_url='/acceso/login.html')
def citas(request):
	user = request.user
	citas=Cita.objects.all()
	if request.GET.get("action") == "crearCita":
		return redirect("Gestion")
	return render(request, "gestion/citas.html", {
		"citas":citas,
		"url_modificar": reverse('CitasModificar'),
  	"rol": user.role.nombre})
 
@login_required(login_url='/acceso/login.html')
def ofertas(request):
	user = request.user
	ofertas=Oferta.objects.all()
	return render(request, "gestion/ofertas.html", {
		"ofertas":ofertas,
  		"url_modificar": reverse('OfertasModificar'),
    "rol": user.role.nombre})

@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def usuarios(request):
	user = request.user
	usuarios=Usuario.objects.all() 
	return render(request, "gestion/usuarios.html", {
		"usuarios":usuarios,
		"url_modificar": reverse('UsuariosModificar'),
  	"rol": user.role.nombre})

@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def accionesOferta(request):
	user = request.user
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearOfertaForm,
		"url_destino": reverse('OfertasCrear'),
		"url_listado": reverse('Ofertas'),
		"tipo" : "oferta",
		"rol": user.role.nombre})

@login_required(login_url='/acceso/login.html')
def accionesCita(request):
	user = request.user
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearCitaForm,
		"url_destino": reverse('CitasCrear'),
		"url_listado": reverse('Citas'),
		"tipo" : "cita",
		"rol": user.role.nombre})
 
@login_required(login_url='/acceso/login.html')
def accionesUsuario(request):
	user = request.user
	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearUsuarioForm,
		"url_destino": reverse('UsuariosCrear'),
		"url_listado": reverse('Usuarios'),
		"tipo" : "usuario",
		"rol": user.role.nombre})

@login_required(login_url='/acceso/login.html')
def accionesServicio(request):
	user = request.user
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
			"tipo" : "servicio",
		"rol": user.role.nombre})
	

	return render(request, "gestion/snippets/creacion.html", {
		"accion":"crear",
		"data":crearServicioForm,
		"url_destino": reverse('ServiciosCrear'),
		"url_listado": reverse('Servicios'),
		"tipo" : "servicio",
		"rol": user.role.nombre})

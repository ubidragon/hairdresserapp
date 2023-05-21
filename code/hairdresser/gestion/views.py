from datetime import date, datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import *
from .cita import proximasCitas, historicoCitas, crearCita, modificarCita, eliminarCita
from .usuario import crearUsuario, modificarUsuario, eliminarUsuario
from .servicio import crearServicio, modificarServicio, eliminarServicio
from .oferta import crearOferta, modificarOferta, eliminarOferta
from .utils_gestion import obtener_objeto_por_id, is_Active, is_admin, is_cliente

# 
# 
# PANTALLA PRINCIPAL DE ACCESO
#
@user_passes_test(is_Active)
@login_required(login_url='/acceso/login.html')
def home(request):
  """Generacion de la landing del Area de usuario.

  Args:
      request (_type_): Peticion GET para la visualizacion de la Home de usuario

  Returns:
      _type_: HttpRequest 
  """  
  # TODO AGREGAR BOTON DE MIS DATOS, PARA QUE CADA USER PUEDA VER SUS PROPIOS DATOS.
  # CON RECUPERAR UN FORMULARIO COMO EL DE MODIFICAR USUARIO DEBERIA DE VALER.
  user = request.user
  return render(request, "gestion/home.html", {"rol": user.role.nombre})
# 
# 
# CITAS
#
@user_passes_test(is_Active)
@login_required(login_url='/acceso/login.html')
def citas(request):
  user = request.user
  if request.GET.get("action") == "crearCita":
    return redirect("Citas")
  elif request.GET.get("action") == "historico":
    return historicoCitas(request, user)
  elif request.GET.get("action") == "proximas":
    return proximasCitas(request, user)
  return render(request, "gestion/citas.html", {"rol": user.role.nombre})
  
@user_passes_test(is_Active)
@login_required(login_url='/acceso/login.html')
def accionesCita(request):
  user = request.user
  if "citas/crear" in request.path :   
    return crearCita(request, user)
       
  elif "citas/modificar" in request.path :
    return modificarCita(request, user)
        
  elif "citas/eliminar" in request.path :
    return eliminarCita(request, user)
  
# 
# 
# USUARIOS
#
@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def usuarios(request):
  user = request.user
  usuarios=Usuario.objects.all() 
  return render(request, "gestion/usuarios.html", {
    "usuarios":usuarios,
    "url_modificar": reverse('UsuariosModificar'),
    "url_eliminar": reverse('UsuariosEliminar'),
    "rol": user.role.nombre})
@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def accionesUsuario(request):
  user = request.user
  if "usuarios/crear" in request.path :
    return crearUsuario(request, user)
  
  elif "usuarios/modificar" in request.path :
    return modificarUsuario(request, user)
  
  elif "usuarios/eliminar" in request.path :
    return eliminarUsuario(request, user)
  
# 
# 
# OFERTAS
#
@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def ofertas(request):
  user = request.user
  ofertas=Oferta.objects.all()
  return render(request, "gestion/ofertas.html", {
    "ofertas":ofertas,
      "url_modificar": reverse('OfertasModificar'),
    "url_eliminar": reverse('OfertasEliminar'),
    "rol": user.role.nombre})
  
@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def accionesOferta(request):
  user = request.user
  if "ofertas/crear" in request.path :
    return crearOferta(request,user)
  
  elif "ofertas/modificar" in request.path :
    return modificarOferta(request,user)
  
  elif "ofertas/eliminar" in request.path :
    return eliminarOferta(request,user)
  
# 
# 
# SERVICIOS
# 
@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def servicios(request):
  user = request.user
  servicios=Servicio.objects.all()
  return render(request, "gestion/servicios.html", {
       "servicios":servicios,
        "url_modificar": reverse('ServiciosModificar'),
    "url_eliminar": reverse('ServiciosEliminar'),
      "rol": user.role.nombre})

@user_passes_test(is_Active)
@user_passes_test(is_admin)
@login_required(login_url='/acceso/login.html')
def accionesServicio(request):
  user = request.user
  referer = request.POST.get('referer')
  # if referer is not None:
  if "servicios/crear" in request.path :
    return crearServicio(request, user)
  
  elif "servicios/modificar" in request.path:
    return modificarServicio(request, user)
  
  elif "servicios/eliminar" in request.path:
    return eliminarServicio(request, user)
  

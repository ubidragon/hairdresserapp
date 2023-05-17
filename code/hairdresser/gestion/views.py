from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from .forms import *
from .utils_gestion import *
# 
# 
# PANTALLA PRINCIPAL DE ACCESO
#
@user_passes_test(is_Active)
@login_required(login_url='/acceso/login.html')
def home(request):
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
  citas=Cita.objects.all()
  if request.GET.get("action") == "crearCita":
    return redirect("Gestion")
  return render(request, "gestion/citas.html", {
    "citas":citas,
    "url_modificar": reverse('CitasModificar'),
    "url_eliminar": reverse('CitasEliminar'),
    "rol": user.role.nombre})
@user_passes_test(is_Active)
@login_required(login_url='/acceso/login.html')
def accionesCita(request):
  # TODO FALTA TODAS LAS ACCIONES DE CITA
  user = request.user
  return render(request, "gestion/snippets/accionesObjetos.html", {
    "accion":"crear",
    "data":crearCitaForm,
    "url_destino": reverse('CitasCrear'),
    "url_listado": reverse('Citas'),
    "tipo" : "cita",
    "rol": user.role.nombre})
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
    if request.method == "GET":
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":crearUsuarioForm,
        "url_destino": reverse('UsuariosCrear'),
        "url_listado": reverse('Usuarios'),
        "tipo" : "usuario",
        "rol": user.role.nombre})
    elif request.method == "POST":
      # TODO RELLENAR CORRECTAMENTE LOS CAMPOS DE CREACION
      nuevoUsuario = crearUsuarioForm(request.POST)
      if nuevoUsuario.is_valid() :
        usuarioObject = Usuario(nombre = nuevoUsuario.cleaned_data['nombre'], fecha_fin = nuevoUsuario.cleaned_data['fecha_fin'], descuento = nuevoUsuario.cleaned_data['descuento'], activo = nuevoUsuario.cleaned_data['activo'])
        usuarioObject.save()
      return redirect("Usuarios")
  elif "usuarios/modificar" in request.path :
    if request.method == "GET":
      # TODO: HACER TODO EL PROCESO DE RECUPERAR CAMPOS
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"modificar",
        # "data":modificarUsuarioForm,
        "url_destino": reverse('UsuariosCrear'),
        "url_listado": reverse('Usuarios'),
        "tipo" : "oferta",
        "rol": user.role.nombre})
    if request.method == "POST":
      # TODO: HACER TODO EL PROCESO DE MDOIFICAR CAMPOS
      pass
  elif "usuarios/eliminar" in request.path :
    if request.method == "GET":
      usuarioDb = obtener_objeto_por_id(Usuario, request.GET.get('id'))
      campos_modelo = usuarioDb._meta.fields     
      atributos = {}
      for campo in campos_modelo:
        # if campo.name not in campos_excluidos:
          atributos[campo.name] = getattr(usuarioDb, campo.name)

      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"eliminar",
        "objeto":usuarioDb,
        "atributos":atributos, 
        "tipo" : "usuario",
        "url_destino": reverse('UsuariosEliminar'),
        "url_listado": reverse('Usuarios'),
        "rol": user.role.nombre})
    elif request.method == "POST":
      usuarioDb = obtener_objeto_por_id(Usuario, request.POST.get('id'))
      # BORRADO LOGICO
      if request.POST.get('activo') == "checked":
        usuarioDb.activo = 1
      else:
        usuarioDb.activo = 0	
      usuarioDb.save()
      return redirect("Usuarios")
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
    if request.method == "GET":
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":crearOfertaForm,
        "url_destino": reverse('OfertasCrear'),
        "url_listado": reverse('Ofertas'),
        "tipo" : "oferta",
        "rol": user.role.nombre})
    elif request.method == "POST":
      nuevaOferta = crearOfertaForm(request.POST)
      if nuevaOferta.is_valid() :
        ofertaObject = Oferta(nombre = nuevaOferta.cleaned_data['nombre'], fecha_fin = nuevaOferta.cleaned_data['fecha_fin'], descuento = nuevaOferta.cleaned_data['descuento'], activo = nuevaOferta.cleaned_data['activo'])
        ofertaObject.save()
      return redirect("Ofertas")
  elif "ofertas/modificar" in request.path :
    if request.method == "GET":
      ofertaDb = obtener_objeto_por_id(Oferta, request.GET.get('id'))
      initial_data = {'activo': ofertaDb.activo}
      elemento = modificarOfertaForm(instance=ofertaDb,initial=initial_data)
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"modificar",
        "data":[elemento],
        "url_destino": reverse('OfertasModificar'),
        "url_listado": reverse('Ofertas'),
        "tipo" : "oferta",
        "rol": user.role.nombre})
    elif request.method == "POST":
      # TODO: HACER TODO EL PROCESO DE MDOIFICAR CAMPOS
      
      pass
  elif "ofertas/eliminar" in request.path :
    if request.method == "GET":
      ofertaDb = obtener_objeto_por_id(Oferta, request.GET.get('id'))
      campos_modelo = ofertaDb._meta.fields     
      atributos = {}
      for campo in campos_modelo:
        # if campo.name not in campos_excluidos:
          atributos[campo.name] = getattr(ofertaDb, campo.name)

      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"eliminar",
        "objeto":ofertaDb,
        "atributos":atributos, 
        "tipo" : "oferta",
        "url_destino": reverse('OfertasEliminar'),
        "url_listado": reverse('Ofertas'),
        "rol": user.role.nombre})
    elif request.method == "POST":
      ofertaDb = obtener_objeto_por_id(Oferta, request.POST.get('id'))
      ofertaDb.delete()
      return redirect("Ofertas")
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
    
    if request.method == "GET":
      return render(request, "gestion/snippets/accionesObjetos.html", {
      "accion":"crear",
      "data":crearServicioForm,
      "url_destino": reverse('ServiciosCrear'),
      "url_listado": reverse('Servicios'),
      "tipo" : "servicio",
      "rol": user.role.nombre})

    elif request.method == "POST":
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
  elif "servicios/modificar" in request.path:
  
    ofertaDbData=""
    ubicacionDbData=""

    if request.method == "GET":
      servicioDb = obtener_objeto_por_id(Servicio, request.GET.get('id'))

      if servicioDb.oferta.first() is not None:
        ofertaDb= obtener_objeto_por_id(Oferta, servicioDb.oferta.first().id)
        ofertaDbData=ofertaDb.nombre
    
      if  servicioDb.ubicacion.nombre is not None:
        ubicacionDbData= servicioDb.ubicacion.nombre
      
      initial_data = {'ubicacion': ubicacionDbData,
          'oferta': ofertaDbData,
          'activo': servicioDb.activo
          }

      elemento = modificarServicioForm(instance=servicioDb,initial=initial_data)
      
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"modificar",
        "data":[elemento],
        "url_destino": reverse('ServiciosModificar'),
        "url_listado": reverse('Servicios'),
        "tipo" : "servicio",
      "rol": user.role.nombre})
   
    elif request.method == "POST":

      servicioDb = obtener_objeto_por_id(Servicio, request.POST.get('id'))

      if servicioDb.oferta.first() is not None:
        ofertaDb= obtener_objeto_por_id(Oferta, servicioDb.oferta.first().id)
        ofertaDbData=ofertaDb.nombre
    
      if  servicioDb.ubicacion.nombre is not None:
        ubicacionDbData= servicioDb.ubicacion.nombre
          
      # Reasignacion de valores en caso de que haya sido cambiado algun atributo
      if servicioDb.nombre != request.POST.get('nombre'):
        servicioDb.nombre = request.POST.get('nombre')
      if servicioDb.precio != request.POST.get('precio'):
        servicioDb.precio = request.POST.get('precio')
      if servicioDb.duracion != request.POST.get('duracion'):
        servicioDb.duracion = request.POST.get('duracion')
      if servicioDb.descripcion != request.POST.get('descripcion'):
        servicioDb.descripcion = request.POST.get('descripcion')
      if request.POST.get('activo') == "checked":
        servicioDb.activo = 1
      else:
        servicioDb.activo = 0	
      if ubicacionDbData != request.POST.get('ubicacion'):
        servicioDb.ubicacion = Ubicacion.objects.get(nombre=request.POST.get('ubicacion'))
      if ofertaDbData != request.POST.get('oferta'):
        servicioDb.oferta.set(request.POST.get('oferta')) 

      # servicioDb.full_clean()
      servicioDb.save()
      return redirect("Servicios")
  elif "servicios/eliminar" in request.path:
    if request.method == "GET":
      servicioDb = obtener_objeto_por_id(Servicio, request.GET.get('id'))
      campos_modelo = servicioDb._meta.fields     
      atributos = {}
      for campo in campos_modelo:
        # if campo.name not in campos_excluidos:
          atributos[campo.name] = getattr(servicioDb, campo.name)

      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"eliminar",
        "objeto":servicioDb,
        "atributos":atributos, 
        "tipo" : "servicio",
        "url_destino": reverse('ServiciosEliminar'),
        "url_listado": reverse('Servicios'),
        "rol": user.role.nombre})
    if request.method == "POST":
      servicioDb = obtener_objeto_por_id(Servicio, request.POST.get('id'))
      servicioDb.delete()
      return redirect("Servicios")

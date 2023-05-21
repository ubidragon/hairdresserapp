from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import crearServicioForm, modificarServicioForm
from .models import Servicio, Ubicacion, Oferta
from .utils_gestion import obtener_objeto_por_id

def crearServicio(request, user):
        
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
  
def modificarServicio(request, user):
  
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

def eliminarServicio(request, user):
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


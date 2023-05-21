
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from datetime import date, datetime, timedelta
from .models import Cita, asigna_citas_empleado
from .forms import crearCitaAdminForm, crearCitaClienteForm, modificarCitaForm, modificarCitaPasada
from .utils_gestion import obtener_objeto_por_id, is_Active, is_admin, is_cliente

def proximasCitas(request, user):
  user = request.user
  fechaProximos7Dias=datetime.now() + timedelta(days=7)
  citas=Cita.objects.filter(Q(fecha_cita__gt=datetime.now().strftime("%Y-%m-%d")) & Q(fecha_cita__lt=fechaProximos7Dias.strftime("%Y-%m-%d")))
  
  return render(request, "gestion/listadoCitas.html", {
    "citas":citas,
    "tipo":"cita",
    "url_listado": reverse('Citas'),
    "url_modificar": reverse('CitasModificar'),
    "url_eliminar": reverse('CitasEliminar'),
    "rol": user.role.nombre})

def historicoCitas(request, user):
  user = request.user
  citas=Cita.objects.all()
  return render(request, "gestion/listadoCitas.html", {
    "citas":citas,
    "tipo":"cita",
    "url_listado": reverse('Citas'),
    "url_modificar": reverse('CitasModificar'),
    "url_eliminar": reverse('CitasEliminar'),
    "rol": user.role.nombre})

def crearCita(request, user):
    if request.method == "GET":
      if is_admin(user):
        return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data": [crearCitaAdminForm],
        "url_destino": reverse('CitasCrear'),
        "url_listado": reverse('Citas'),
        "tipo" : "cita",
        "rol": user.role.nombre})
      elif is_cliente(user):
        return render(request, "gestion/snippets/accionesObjetos.html", {
          "accion":"crear",
          "data":crearCitaClienteForm(initial={'cliente': request.user.id}),
          "url_destino": reverse('CitasCrear'),
          "url_listado": reverse('Citas'),
          "tipo" : "cita",
          "rol": user.role.nombre})
    elif request.method == "POST":
      nuevaCita = crearCitaAdminForm(request.POST)

      if nuevaCita.is_valid() :
          empleadoId=nuevaCita.cleaned_data['empleado'].id
          # Creamos un nuevo objecto 
          citaObject = Cita(estado="Programada",fecha_cita=nuevaCita.cleaned_data['fecha_cita'],cliente_id=nuevaCita.cleaned_data['cliente'].id, servicio=nuevaCita.cleaned_data['servicio'])
          # Guardamos en base de datos
          citaObject.save()
          # Asignamos la cita al empleado seleccionado en el formulario tomando el id de la nueva cita ya almacenada.
          nuevaCitaAsignada= asigna_citas_empleado(cita_id=citaObject.id,empleado_id=empleadoId)
          # Guardamos en base de datos
          nuevaCitaAsignada.save()  
          return redirect('Citas')
      else:
        # En caso de que no sea valido se volvera a cargar el formulario para que muestre los errores
        return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":crearCitaAdminForm,
        "url_destino": reverse('CitasCrear'),
        "url_listado": reverse('Citas'),
        "tipo" : "cita",
        "rol": user.role.nombre})
              
def modificarCita(request, user):
    if request.method == "GET":
      
      citaDb = obtener_objeto_por_id(Cita, request.GET.get('id'))
      empleadoDB = asigna_citas_empleado.objects.get(cita_id=citaDb.id)
      fecha_formateada = citaDb.fecha_cita.strftime("%Y-%m-%d")
      initial_data = {'id': citaDb.id,'servicio': citaDb.servicio.id,'cliente':citaDb.cliente.id, 'empleado':empleadoDB.empleado_id, 'fecha_cita': fecha_formateada}

      elemento = modificarCitaForm(instance=citaDb,initial=initial_data)
 
      if str(citaDb.fecha_cita) < datetime.now().strftime("%Y-%m-%d") or citaDb.estado == "Cancelada":
        return render(request, "gestion/snippets/accionesObjetos.html", {
            "accion":"modificar",
            "volver": "volver",
            "data":[modificarCitaPasada(instance=citaDb,initial=initial_data)],
            "url_destino": reverse('Citas'),
            "url_listado": reverse('Citas'),
            "tipo" : "cita",
            "rol": user.role.nombre})
 
      if is_admin(user):
        is_admin
        return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"modificar",
        "data":[elemento],
        "url_destino": reverse('CitasModificar'),
        "url_listado": reverse('Citas'),
        "tipo" : "cita",
        "rol": user.role.nombre})
      elif is_cliente(user):
        return render(request, "gestion/snippets/accionesObjetos.html", {
          "accion":"modificar",
          "data":crearCitaClienteForm(initial={'cliente': request.user.id}),
          "url_destino": reverse('CitasModificar'),
          "url_listado": reverse('Citas'),
          "tipo" : "cita",
          "rol": user.role.nombre})
    elif request.method == "POST":
      
      citaDb= obtener_objeto_por_id(Cita, request.POST.get('id'))
      citaModificada = modificarCitaForm(request.POST)
          
      
      # Comprobacion que la nueva fecha es una fecha futura
      if request.POST.get('fecha_cita') < datetime.now().strftime("%Y-%m-%d"):
          citaPrevia = modificarCitaForm(request.POST)
          citaPrevia.add_error("fecha_cita","Se ha introducido una fecha pasada. Solo se pueden incluir fechas a futuro.")
          return render(request, "gestion/snippets/accionesObjetos.html", {
            "accion":"modificar",
            "data":[citaPrevia],
            "url_destino": reverse('CitasModificar'),
            "url_listado": reverse('Citas'),
            "tipo" : "cita",
            "rol": user.role.nombre})
          
      if citaModificada.is_valid():
        citaDb= obtener_objeto_por_id(Cita, request.POST.get('id'))
        empleadoDB = asigna_citas_empleado.objects.get(cita_id=citaDb.id)
        
        if citaDb.servicio.id != request.POST.get('servicio'):
          citaDb.servicio.id = request.POST.get('servicio')
        if citaDb.cliente_id != request.POST.get('cliente'):
          citaDb.cliente_id = request.POST.get('cliente')
        if citaDb.fecha_cita != request.POST.get('fecha_cita'):
          citaDb.fecha_cita = request.POST.get('fecha_cita')
        if empleadoDB.empleado != request.POST.get('empleado'):
          empleadoDB.empleado_id = request.POST.get('empleado')

          
        citaDb.save()
        empleadoDB.save()
        
        return redirect("Citas")
      else:
        return render(request, "gestion/snippets/accionesObjetos.html", {
          "accion":"modificar",
          "data":modificarCitaForm,
          "url_destino": reverse('CitasModificar'),
          "url_listado": reverse('Citas'),
          "tipo" : "cita",
          "rol": user.role.nombre})
  
#  TODO: Implementar funcionalidad de eliminacion de cita, que realmente lo que hace es cancelarla, para asi mantener un historico.
def eliminarCita(request, user):
    if request.method == "GET":
      citaDb = obtener_objeto_por_id(Cita, request.GET.get('id'))
      empleadoDB = asigna_citas_empleado.objects.get(cita_id=citaDb.id)
      fecha_formateada = citaDb.fecha_cita.strftime("%Y-%m-%d")
      initial_data = {'id': citaDb.id,'servicio': citaDb.servicio.id,'cliente':citaDb.cliente.id, 'empleado':empleadoDB.empleado_id, 'fecha_cita': fecha_formateada}

      return render(request, "gestion/snippets/accionesObjetos.html", {
            "accion":"modificar",
            "volver": "volver",
            "data":[modificarCitaPasada(instance=citaDb,initial=initial_data)],
            "url_destino": reverse('Citas'),
            "url_listado": reverse('Citas'),
            "tipo" : "cita",
            "rol": user.role.nombre})
    if request.method == "POST":
      citaDb = obtener_objeto_por_id(Cita, request.POST.get('id'))
      citaDb.estado = "Cancelada"
      citaDb.save()
      return redirect("Citas")
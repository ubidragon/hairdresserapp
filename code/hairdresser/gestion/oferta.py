from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import crearOfertaForm, modificarOfertaForm
from .models import Oferta
from .utils_gestion import obtener_objeto_por_id


def crearOferta(request, user):
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
      else:
        return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":nuevaOferta,
        "url_destino": reverse('OfertasCrear'),
        "url_listado": reverse('Ofertas'),
        "tipo" : "oferta",
        "rol": user.role.nombre})
        
def modificarOferta(request, user):
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


def eliminarOferta(request, user):
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
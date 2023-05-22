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
        # Guardado en base de datos
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
      fecha_formateada = ofertaDb.fecha_fin.strftime("%Y-%m-%d")
      initial_data = {'fecha_fin':fecha_formateada,'activo': ofertaDb.activo}
      elemento = modificarOfertaForm(instance=ofertaDb,initial=initial_data)
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"modificar",
        "data":[elemento],
        "url_destino": reverse('OfertasModificar'),
        "url_listado": reverse('Ofertas'),
        "tipo" : "oferta",
        "rol": user.role.nombre})
    elif request.method == "POST":
        ofertaModificada = modificarOfertaForm(request.POST)
      
        if ofertaModificada.is_valid() : 
            ofertaDb = obtener_objeto_por_id(Oferta, request.POST.get('id'))
            # Comprobaciones para detectar si algun campo ha sufrido alguna modificacion.    
            if ofertaDb.nombre != request.POST.get('nombre'):
                ofertaDb.nombre = request.POST.get('nombre')
            if ofertaDb.descuento != request.POST.get('descuento'):
                ofertaDb.descuento = request.POST.get('descuento')
            if ofertaDb.fecha_fin != request.POST.get('fecha_fin'):
                ofertaDb.fecha_fin = request.POST.get('fecha_fin')      
            if request.POST.get('activo') == "checked":
                ofertaDb.activo = 1
            else:
                ofertaDb.activo = 0	
            # Guardado en base de datos
            ofertaDb.save()
            return redirect('Ofertas')
        else:
            return render(request, "gestion/snippets/accionesObjetos.html", {
            "accion":"modificar",
            "data":[modificarOfertaForm],
            "url_destino": reverse('OfertasModificar'),
            "url_listado": reverse('Ofertas'),
            "tipo" : "oferta",
            "rol": user.role.nombre})

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
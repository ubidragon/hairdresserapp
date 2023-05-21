from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import crearUsuarioForm, modificarUsuarioForm
from .models import Usuario, Roles
from .utils_gestion import obtener_objeto_por_id

def crearUsuario(request, user):
    if request.method == "GET":
      return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":crearUsuarioForm,
        "url_destino": reverse('UsuariosCrear'),
        "url_listado": reverse('Usuarios'),
        "tipo" : "usuario",
        "rol": user.role.nombre})
    elif request.method == "POST":
      nuevoUsuario = crearUsuarioForm(request.POST)
      if nuevoUsuario.is_valid() :
            
        role_nombre = nuevoUsuario.cleaned_data['role']
        roleObject = Roles.objects.get(nombre=role_nombre)
                
        usuarioObject = Usuario(nombre = nuevoUsuario.cleaned_data['nombre'], apellidos = nuevoUsuario.cleaned_data['apellidos'], fecha_nacimiento = nuevoUsuario.cleaned_data['fecha_nacimiento'], password = nuevoUsuario.cleaned_data['password'], email = nuevoUsuario.cleaned_data['email'], role = roleObject, movil = nuevoUsuario.cleaned_data['movil'], activo = nuevoUsuario.cleaned_data['activo'])
        
        usuarioObject.save()
        return redirect("Usuarios")
      else:
      # Retornamos a la pantalla de creacion para que se puedan mostrar los errores recogidos al validar el formulario en el backend
        return render(request, "gestion/snippets/accionesObjetos.html", {
        "accion":"crear",
        "data":nuevoUsuario,
        "url_destino": reverse('UsuariosCrear'),
        "url_listado": reverse('Usuarios'),
        "tipo" : "usuario",
        "rol": user.role.nombre})
        
def modificarUsuario(request, user):
	if request.method == "GET":
		usuarioDb = obtener_objeto_por_id(Usuario, request.GET.get('id'))
		fechaFormateada=usuarioDb.fecha_nacimiento.strftime("%Y-%m-%d")
		initial_data = {'id': usuarioDb.id, 'fecha_nacimiento' : fechaFormateada, 'movil':usuarioDb.movil,'activo': usuarioDb.activo}
		elemento = modificarUsuarioForm(instance=usuarioDb,initial=initial_data)
		elemento.fields['password'].widget.attrs['value'] = usuarioDb.password
  
		return render(request, "gestion/snippets/accionesObjetos.html", {
		"accion":"modificar",
		"data":[elemento],
		"url_destino": reverse('UsuariosModificar'),
		"url_listado": reverse('Usuarios'),
		"tipo" : "usuario",
		"rol": user.role.nombre})
    
	elif request.method == "POST":
		usuarioDb = obtener_objeto_por_id(Usuario, request.POST.get('id'))
		usuarioModificado = modificarUsuarioForm(request.POST)
		eroare = usuarioModificado.errors.values()
  
		if usuarioModificado.is_valid():
			if usuarioDb.nombre != request.POST.get('nombre'):
				usuarioDb.nombre = request.POST.get('nombre')

			if usuarioDb.apellidos != request.POST.get('apellidos'):
				usuarioDb.apellidos = request.POST.get('apellidos')

			if usuarioDb.fecha_nacimiento != request.POST.get('fecha_nacimiento'):
				usuarioDb.fecha_nacimiento = request.POST.get('fecha_nacimiento')

			if usuarioDb.password != request.POST.get('password'):
				usuarioDb.password = request.POST.get('password')

			if usuarioDb.email != request.POST.get('email'):
				usuarioDb.email = request.POST.get('email')

			if usuarioDb.movil != request.POST.get('movil'):
				usuarioDb.movil = request.POST.get('movil')

			if usuarioDb.role.id != request.POST.get('role'):
				usuarioDb.role.id = request.POST.get('role')

			if request.POST.get('activo') == "checked":
				usuarioDb.activo = 1
			else:
				usuarioDb.activo = 0	

			usuarioDb.save()
			return redirect("Usuarios")
		else:
			elemento = modificarUsuarioForm(request.POST)
			elemento.fields['password'].widget.attrs['value'] = request.POST.get('password')
			return render(request, "gestion/snippets/accionesObjetos.html", {
			"accion":"modificar",
			"data":[elemento],
			"url_destino": reverse('UsuariosModificar'),
			"url_listado": reverse('Usuarios'),
			"tipo" : "usuario",
			"rol": user.role.nombre})
		


def eliminarUsuario(request, user):
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

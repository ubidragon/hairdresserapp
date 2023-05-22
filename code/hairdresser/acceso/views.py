from django.shortcuts import render, redirect
from .forms import inicioSesion, registro
from gestion.models import Usuario, Roles
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def inicio(request):
    if request.method == 'GET':
        formularioLogin=inicioSesion()
        return render(request, "acceso/login.html", {'formularioInicio':formularioLogin})
    elif request.method == 'POST':
        formularioLogin=inicioSesion(request.POST)
        if formularioLogin.is_valid():
            formEmail=formularioLogin.cleaned_data.get("email")
            formPasswd=formularioLogin.cleaned_data.get("passwd")
            usuario=Usuario.objects.filter(email=formEmail).first()
            if usuario is not None :
                if usuario.activo == True:
                    usuarioPasswd=usuario.password
                    if usuarioPasswd == formPasswd:                                
                        login(request, usuario)
                        if "login" in request.path:
                            return redirect('Gestion')
                        else:
                            return redirect(request.GET.get('next', '/'))
                    else:
                        messages.error(request, formularioLogin.add_error("passwd","Usuario/Contraseña no correcta"))
                else:
                    messages.error(request, formularioLogin.add_error("passwd","Usuario inactivado. Contacte con el administrador del sitio"))
            else:
                messages.error(request, formularioLogin.add_error("passwd","Usuario/Contraseña no correcta"))
        return render(request, "acceso/login.html", {'formularioInicio':formularioLogin})

def cerrarSesion(request):
    logout(request)
    return redirect("Inicio")

def signUp(request):
    
    if request.method == 'GET':
        formularioRegistro=registro()
        return render(request, "acceso/signup.html", {'formularioRegistro':formularioRegistro})
    elif request.method == 'POST':
        # form=UserCreationForm()
        formularioRegistro=registro(request.POST)
        
        if formularioRegistro.is_valid():
            password = request.POST.get('passwd')
            passwordRepeat = request.POST.get('repeatPasswd')
            
            if password == passwordRepeat:
                existeUsuario = Usuario.objects.filter(email=request.POST.get('email')).exists()
                if not existeUsuario:
                    nuevoUsuario = Usuario( nombre = formularioRegistro.cleaned_data['nombre'], 
                            apellidos = formularioRegistro.cleaned_data['apellidos'], 
                            password = formularioRegistro.cleaned_data['passwd'], 
                            fecha_nacimiento = formularioRegistro.cleaned_data['nacimiento'], 
                            movil = formularioRegistro.cleaned_data['movil'], 
                            email = formularioRegistro.cleaned_data['email'],
                            role = Roles.objects.filter(nombre = "cliente").first(),
                            activo = 1)
                    
                    nuevoUsuario.save()
    
                    login(request,nuevoUsuario)
                    return redirect('Gestion')
                else:
                    messages.error(request, formularioRegistro.add_error("email","El usuario ya existe en el sistema.\n¿Has probado a iniciar sesión?."))
            else:
                messages.error(request, formularioRegistro.add_error("repeatPasswd","Las contraseñas deben de ser iguales."))   
        return render(request, "acceso/signup.html", {'formularioRegistro':formularioRegistro})
        
        # # TODO: Construir el formulario de registro con sus validaciones.
        # if len(request.GET) > 0:
        #     return render(request, "acceso/signup.html", {'formularioRegistro':signup})
        # elif signup.is_valid():
        #     login(request)
        #     return redirect('Gestion')
        # else:
        #     for error in signup.errors:
        #         messages.error(request, signup.errors[error])
        #     return render(request, "acceso/signup.html", {'formularioRegistro':signup})
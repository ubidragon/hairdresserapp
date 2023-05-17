from django.shortcuts import render, redirect
from .forms import inicioSesion, registro
from gestion.models import Usuario
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def inicio(request):
    formularioLogin=inicioSesion()
    if request.method == 'POST':
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
    else:    
        return render(request, "acceso/login.html", {'formularioInicio':formularioLogin})

def cerrarSesion(request):
    logout(request)
    return redirect("Inicio")

def signUp(request):
    # form=UserCreationForm()
    signup=registro(request.POST)
    
    if len(request.GET) > 0:
        return render(request, "acceso/signup.html", {'formularioRegistro':signup})
    elif signup.is_valid():
        login(request)
        return redirect('Gestion')
    else:
        for error in signup.errors:
            messages.error(request, signup.errors[error])
        return render(request, "acceso/signup.html", {'formularioRegistro':signup})
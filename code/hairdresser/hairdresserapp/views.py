from django.shortcuts import render,  redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from .forms import FormularioContacto
# render_to_response,
# Create your views here.


def home(request):
    
    return render(request, "hairdresserapp/home.html")

def servicios(request):
    
    return render(request, "hairdresserapp/servicios.html")

def contacto(request):
    formulario_Contacto=FormularioContacto()
    
    if request.method == "POST":
        formulario_Relleno=FormularioContacto(data=request.POST)
        if formulario_Relleno.is_valid():
            nombre = request.POST.get("nombre")
            senderEmail = request.POST.get("email")
            mensaje =  request.POST.get("mensaje")
            
            email=EmailMessage("Mensaje desde panel de contacto",
                               "El usuario {} con la direccion {} ha escrito:\n\n{}".format(nombre,senderEmail,mensaje), senderEmail, ["info.hairdresserapp@gmail.com"], reply_to=[senderEmail])
            
            try:
                return redirect("/contacto?correcto")
            except:
                return redirect("/contacto?incorrecto")
    
    return render(request, "hairdresserapp/contacto.html", {'formularioContacto':formulario_Contacto})


# #404: página no encontrada
# def pag_404_not_found(request, exception, template_name="error/404.html"):
#     response = render_to_response("error/404.html")
#     response.status_code=404
#     return response
 
# #500: error en el servidor
# def pag_500_error_server(request, exception,template_name="error/500.html"):
#     response = render_to_response("error/500.html")
#     response.status_code=500
#     return response
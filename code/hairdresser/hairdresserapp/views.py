from django.shortcuts import render,  HttpResponse
# render_to_response,
# Create your views here.


def home(request):
    
    return render(request, "hairdresserapp/home.html")

def servicios(request):
    
    return render(request, "hairdresserapp/servicios.html")

def contacto(request):
    
    return render(request, "hairdresserapp/contacto.html")


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
from django.urls import path
# from django.conf.urls import handler404, handler500
from hairdresserapp import views

urlpatterns = [
    path('', views.home, name="Inicio"),
    path('servicios', views.servicios, name="ServiciosWeb"),
    path('contacto', views.contacto, name="Contacto"),
]

# handler404 = 'views.pag_404_not_found'
# handler500 = 'views.pag_500_error_server'

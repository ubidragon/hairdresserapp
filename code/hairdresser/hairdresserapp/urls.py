from django.urls import path

from hairdresserapp import views

urlpatterns = [
    path('', views.home, name="Inicio"),
    path('servicios', views.servicios, name="Servicios"),
    path('contacto', views.contacto, name="Contacto"),
]
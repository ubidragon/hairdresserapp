from django.urls import path, re_path

from gestion import views

urlpatterns = [
    path('', views.home, name="Gestion"),
    path('citas', views.citas, name="Citas"),
    path('servicios', views.servicios, name="Servicios"),
    path('servicios/crear', views.accionesServicio, name="ServiciosCrear"),
    path('servicios/modificar', views.accionesServicio, name="ServiciosModificar"),
    path('ofertas', views.ofertas, name="Ofertas"),
    path('ofertas/crear', views.accionesOferta, name="OfertasCrear"),
    path('ofertas/modificar', views.accionesOferta, name="OfertasModificar"),
    path('usuarios', views.usuarios, name="Usuarios"),
    
]
from django.urls import path

from hairdresserapp_gestionCitas import views

urlpatterns = [
    path('', views.home, name="Gestion"),
    # path('citas', views.citas, name="Citas"),
    # path('servicios', views.servicios, name="Servicios"),
    # path('ofertas', views.ofertas, name="Ofertas"),
    # path('usuarios', views.usuarios, name="Usuarios"),
]
from django.urls import path

from gestion import views

urlpatterns = [
    path('', views.home, name="Gestion"),
    path('citas', views.citas, name="Citas"),
    path('citas/crear', views.accionesCita, name="CitasCrear"),
    path('citas/modificar', views.accionesCita, name="CitasModificar"),
    path('citas/eliminar', views.accionesCita, name="CitasEliminar"),
    path('servicios', views.servicios, name="Servicios"),
    path('servicios/crear', views.accionesServicio, name="ServiciosCrear"),
    path('servicios/modificar', views.accionesServicio, name="ServiciosModificar"),
    path('servicios/eliminar', views.accionesServicio, name="ServiciosEliminar"),
    path('ofertas', views.ofertas, name="Ofertas"),
    path('ofertas/crear', views.accionesOferta, name="OfertasCrear"),
    path('ofertas/modificar', views.accionesOferta, name="OfertasModificar"),
    path('ofertas/eliminar', views.accionesOferta, name="OfertasEliminar"),
    path('usuarios', views.usuarios, name="Usuarios"),
    path('usuarios/crear', views.accionesUsuario, name="UsuariosCrear"),
    path('usuarios/modificar', views.accionesUsuario, name="UsuariosModificar"),
    path('usuarios/eliminar', views.accionesUsuario, name="UsuariosEliminar"),
    path('profile', views.profile, name="MisDatos"),
]
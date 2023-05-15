from django.urls import path
# from django.conf.urls import handler404, handler500
from acceso import views

urlpatterns = [
    path('login', views.inicio, name="Login"),
    path('signup', views.signUp, name="SignUp"),
    path('logout', views.cerrarSesion, name="LogOut"),
]

# handler404 = 'views.pag_404_not_found'
# handler500 = 'views.pag_500_error_server'

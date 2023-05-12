from django.contrib import admin

from .models  import Cita, Oferta, Roles, Servicio, Ubicacion, Usuario

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("created", "updated")
    

class RolAdmin(admin.ModelAdmin):
    readonly_fields=("created", "updated")  


class CitaAdmin(admin.ModelAdmin):
    pass 
      
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Roles, RolAdmin)
admin.site.register(Cita, CitaAdmin)
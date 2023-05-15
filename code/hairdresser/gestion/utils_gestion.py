


def obtener_objeto_por_id(Modelo, id):
		try:
				objeto = Modelo.objects.get(id=id)
				return objeto
		except Modelo.DoesNotExist:
				return None

def is_admin(user):
    return user.is_authenticated and user.role.nombre == "administrador"

def is_empleado(user):
    return user.is_authenticated and user.role.nombre == "empleado"
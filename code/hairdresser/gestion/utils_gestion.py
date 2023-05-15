


def obtener_objeto_por_id(Modelo, id):
		try:
				objeto = Modelo.objects.get(id=id)
				return objeto
		except Modelo.DoesNotExist:
				return None
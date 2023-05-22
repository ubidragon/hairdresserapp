from .models import Cita
from django.db.models import Q
from datetime import date, datetime

def terminarCitasPasadas():
	"""Tarea programada para que las citas pasadas en el tiempo y que no tengan el estado "Cancelada",
 	   pasen de forma automatica al estado "Realizada"
	"""    
	fecha_actual = date.today()
	citasProgramadas= Cita.objects.filter(Q(estado="Programada"))
	for cita in citasProgramadas:

		if fecha_actual > cita.fecha_cita:
			cita.estado = "Realizada"
   			# Guardado en base de datos
			cita.save()
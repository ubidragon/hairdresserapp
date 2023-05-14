from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Roles(models.Model):
	nombre=models.CharField(max_length=255, blank=False, null=False)
	activo=models.BooleanField(default=True,null=False)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
 
	class Meta:
		verbose_name="roles"
		verbose_name_plural="roles"
		db_table = "rol"


class Usuario(models.Model):
	nombre=models.CharField(max_length=100, blank=False, null=False)
	apellidos=models.CharField(max_length=255, blank=False, null=False)
	passwd=models.CharField(max_length=500,)
	email=models.EmailField( null=False, unique=True)
	role = models.ForeignKey(
		Roles,
		on_delete=models.PROTECT,
	)

	fecha_nacimiento=models.DateField( null=True)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	activo=models.BooleanField(default=True,null=False)


	class Meta:
		verbose_name="usuario"
		verbose_name_plural="usuarios"
		db_table = "usuario"

class Oferta(models.Model):
	nombre=models.CharField(max_length=60, blank=False, null=False)
	fecha_fin=models.DateField(null=True)
	descuento=models.FloatField(null=False)
	activo=models.BooleanField(default=True,null=False)
	updated=models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.nombre
 
	class Meta:
		verbose_name="oferta"
		verbose_name_plural="ofertas"
		db_table = "oferta"

class Ubicacion(models.Model):
	nombre=models.CharField(max_length=255, blank=False, null=False)
	updated=models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.nombre
 
	class Meta:
		verbose_name="ubicacion"
		verbose_name_plural="ubicaciones"
		db_table = "ubicacion"

class Servicio(models.Model):
	nombre=models.CharField(max_length=255, blank=False, null=False)
	descripcion=models.CharField(max_length=1000, blank=False, null=True)
	duracion=models.SmallIntegerField(null=False)
	precio=models.FloatField(null=False)
	ubicacion = models.ForeignKey(
		Ubicacion,
		on_delete=models.PROTECT,
	)
	oferta = models.ManyToManyField(
		Oferta
	)
	activo=models.BooleanField(default=True,null=False)
	updated=models.DateTimeField(auto_now_add=True)
 
	class Meta:
		verbose_name="servicio"
		verbose_name_plural="servicios"
		db_table = "servicio"


class Cita(models.Model):

	class Estado(models.TextChoices):
		PROGRAMADA = "Programada"
		CANCELADA = "Cancelada"
		REALIZADA = "Realizada"

	fecha_cita=models.DateField(null=False)
	estado=models.CharField(
		max_length=12,
		choices=Estado.choices,
		default=Estado.PROGRAMADA,
    )
	servicio = models.ForeignKey(
		to=Servicio,
		on_delete=models.PROTECT,
	)
	cliente = models.ForeignKey(
		Usuario,
		on_delete=models.PROTECT
	)


	class Meta:
		verbose_name="cita"
		verbose_name_plural="citas"
		db_table = "cita"
  
class asigna_citas_empleado(models.Model):
	cita = models.ForeignKey(
		Cita,
		on_delete=models.PROTECT
	)
     
	empleado = models.ForeignKey(
		Usuario,
		on_delete=models.PROTECT
	)
 
	class Meta:
		verbose_name="asigna_citas_empleado"
		db_table = "asigna_citas_empleado"
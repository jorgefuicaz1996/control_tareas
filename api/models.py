from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Region(models.Model):
	id_region = models.IntegerField(primary_key = True)
	nombre = models.CharField(max_length = 50)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'region'

class Comuna(models.Model):
	id_comuna = models.IntegerField(primary_key = True)
	nombre = models.CharField(max_length = 50)
	region = models.ForeignKey(Region, on_delete = models.DO_NOTHING)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'comuna'

class Empresa(models.Model):
	id_empresa = models.AutoField(primary_key = True)
	rut = models.CharField(max_length = 10, unique = True)
	nombre = models.CharField(max_length = 50)
	direccion = models.CharField(max_length = 70)
	comuna = models.ForeignKey(Comuna, on_delete = models.DO_NOTHING)

	class Meta:
		db_table = 'empresa'

class RolFuncionario(models.Model):
	id_rol = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 20)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'rol_funcionario'

class Funcionario(models.Model):
	id_funcionario = models.AutoField(primary_key = True)
	run = models.CharField(max_length = 10, unique = True)
	nombres = models.CharField(max_length = 30)
	ap_paterno = models.CharField(max_length = 30)
	ap_materno = models.CharField(max_length = 30)
	direccion = models.CharField(max_length = 70)
	email = models.EmailField(max_length = 50)
	telefono_movil = models.IntegerField()
	telefono_fijo = models.IntegerField(null = True, blank = True)
	comuna = models.ForeignKey(Comuna, on_delete = models.DO_NOTHING)
	rol = models.ForeignKey(RolFuncionario, on_delete = models.DO_NOTHING)
	empresa = models.ForeignKey(Empresa, on_delete = models.DO_NOTHING)
	usuario = models.OneToOneField(User, on_delete = models.DO_NOTHING)

	def __str__(self):
		return '{} {} {}'.format(self.nombres, self.ap_paterno, self.ap_materno)

	class Meta:
		db_table = 'funcionario'

class RolDepto(models.Model):
	id_rol = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 50)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'rol_depto'

class EstadoTarea(models.Model):
	id_estado = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 20)

	def __str__(self):
		return self.descripcion

	class Meta:
		db_table = 'estado_tarea'

class Tarea(models.Model):
	id_tarea = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 100)
	fecha_inicio = models.DateField()
	fecha_termino = models.DateField(null = True, blank = True)
	fecha_plazo = models.DateField()
	duracion_dias = models.IntegerField()
	estado = models.ForeignKey(EstadoTarea, on_delete = models.DO_NOTHING)
	responsables = models.ManyToManyField(Funcionario, through = 'ResponsableTarea')

	def __str__(self):
		return self.descripcion

	class Meta:
		db_table = 'tarea'

class ResponsableTarea(models.Model):
	funcionario = models.ForeignKey(Funcionario, on_delete = models.DO_NOTHING)
	tarea = models.ForeignKey(Tarea, on_delete = models.DO_NOTHING)

	class Meta:
		db_table = 'responsable_tarea'
		constraints = [
			models.UniqueConstraint( fields = ['funcionario', 'tarea'],name = 'funcionario_tarea_UN')
		]

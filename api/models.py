from django.db import models
from django.contrib.auth.models import User
from powertask import settings

# Create your models here.
if settings.DB_ORACLE:
	class RolDepto(models.Model):
		id_rol = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 50)

		class Meta:
			db_table = 'rol_depto'
			managed = False

		def __str__(self):
			return self.nombre

	class RolFuncionario(models.Model):
		id_rol = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 40)

		class Meta:
			db_table = 'rol_funcionario'
			managed = False

		def __str__(self):
			return self.nombre

	class EstadoTarea(models.Model):
		id_estado = models.AutoField(primary_key = True)
		descripcion = models.CharField(max_length = 20)

		class Meta:
			db_table = 'estado_tarea'
			managed = False

		def __str__(self):
			return self.descripcion

	class Region(models.Model):
		id_region = models.IntegerField(primary_key = True)
		nombre = models.CharField(max_length = 50)

		class Meta:
			db_table = 'region'
			managed = False

		def __str__(self):
			return self.nombre

	class Comuna(models.Model):
		id_comuna = models.IntegerField(primary_key = True)
		nombre = models.CharField(max_length = 50)
		region = models.ForeignKey(Region, on_delete = models.CASCADE, db_column = 'id_region')

		class Meta:
			db_table = 'comuna'
			managed = False

		def __str__(self):
			return self.nombre

	class Empresa(models.Model):
		id_empresa = models.AutoField(primary_key = True)
		rut = models.CharField(max_length = 10, unique = True)
		nombre = models.CharField(max_length = 50)
		direccion = models.CharField(max_length = 70)
		comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, db_column = 'id_comuna')

		class Meta:
			db_table = 'empresa'
			managed = False

		def __str__(self):
			return self.nombre

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
		comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, db_column = 'id_comuna')
		rol = models.ForeignKey(RolFuncionario, on_delete = models.CASCADE, db_column = 'id_rol')
		empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE, db_column = 'id_empresa')
		usuario = models.OneToOneField(User, on_delete = models.CASCADE, db_column = 'user_id')

		class Meta:
			db_table = 'funcionario'
			managed = False

		def __str__(self):
			return '{} {} {}'.format(self.nombres, self.ap_paterno, self.ap_materno)

	class Departamento(models.Model):
		id_depto = models.AutoField(primary_key = True)
		nombre_depto = models.CharField(max_length = 50)
		rol = models.ForeignKey(RolDepto, on_delete = models.CASCADE, db_column = 'id_rol')
		empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE, db_column = 'id_empresa')

		class Meta:
			db_table = 'departamento'
			managed = False

		def __str__(self):
			return self.nombre_depto

	class Funcion(models.Model):
		id_funcion = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 30)
		descripcion = models.CharField(max_length = 100)
		depto = models.ForeignKey(Departamento, on_delete = models.CASCADE, db_column = 'id_depto')

		class Meta:
			db_table = 'funcion'
			managed = False

		def __str__(self):
			return self.nombre

	class Tarea(models.Model):
		id_tarea = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 30)
		descripcion = models.CharField(max_length = 100)
		fecha_inicio = models.DateField()
		fecha_termino = models.DateField(null = True, blank = True)
		fecha_plazo = models.DateField()
		duracion_dias = models.IntegerField()
		estado = models.ForeignKey(EstadoTarea, on_delete = models.CASCADE, db_column = 'id_estado')
		responsables = models.ManyToManyField(Funcionario, through = 'ResponsableTarea')

		class Meta:
			db_table = 'tarea'
			managed = False

		def __str__(self):
			return self.descripcion

	class ResponsableTarea(models.Model):
		funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE, db_column = 'id_funcionario')
		tarea = models.ForeignKey(Tarea, on_delete = models.CASCADE, db_column = 'id_tarea')
		justificativo = models.CharField(max_length = 50, null = True, blank = True)
		plazo_dias = models.IntegerField()

		class Meta:
			db_table = 'responsable_tarea'
			constraints = [
				models.UniqueConstraint(name = 'funcionario_tarea_un', fields = ('funcionario', 'tarea'))
			]
			managed = False

	class Problema(models.Model):
		id_problema = models.AutoField(primary_key = True)
		descripcion = models.CharField(max_length = 500)
		estado = models.CharField(max_length = 15)
		solucion_planteada = models.CharField(max_length = 500),
		funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
		tarea = models.ForeignKey(Tarea, on_delete = models.CASCADE)

		class Meta:
			db_table = 'problema'
			managed = False
else:
	class RolDepto(models.Model):
		id_rol = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 50)

		class Meta:
			db_table = 'rol_depto'

		def __str__(self):
			return self.nombre

	class RolFuncionario(models.Model):
		id_rol = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 40)

		class Meta:
			db_table = 'rol_funcionario'

		def __str__(self):
			return self.nombre

	class EstadoTarea(models.Model):
		id_estado = models.AutoField(primary_key = True)
		descripcion = models.CharField(max_length = 20)

		class Meta:
			db_table = 'estado_tarea'

		def __str__(self):
			return self.descripcion

	class Region(models.Model):
		id_region = models.IntegerField(primary_key = True)
		nombre = models.CharField(max_length = 50)

		class Meta:
			db_table = 'region'

		def __str__(self):
			return self.nombre

	class Comuna(models.Model):
		id_comuna = models.IntegerField(primary_key = True)
		nombre = models.CharField(max_length = 50)
		region = models.ForeignKey(Region, on_delete = models.CASCADE, db_column = 'id_region')

		class Meta:
			db_table = 'comuna'

		def __str__(self):
			return self.nombre

	class Empresa(models.Model):
		id_empresa = models.AutoField(primary_key = True)
		rut = models.CharField(max_length = 10, unique = True)
		nombre = models.CharField(max_length = 50)
		direccion = models.CharField(max_length = 70)
		comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, db_column = 'id_comuna')

		class Meta:
			db_table = 'empresa'

		def __str__(self):
			return self.nombre

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
		comuna = models.ForeignKey(Comuna, on_delete = models.CASCADE, db_column = 'id_comuna')
		rol = models.ForeignKey(RolFuncionario, on_delete = models.CASCADE, db_column = 'id_rol')
		empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE, db_column = 'id_empresa')
		usuario = models.OneToOneField(User, on_delete = models.CASCADE, db_column = 'user_id')

		class Meta:
			db_table = 'funcionario'

		def __str__(self):
			return '{} {} {}'.format(self.nombres, self.ap_paterno, self.ap_materno)

	class Departamento(models.Model):
		id_depto = models.AutoField(primary_key = True)
		nombre_depto = models.CharField(max_length = 50)
		rol = models.ForeignKey(RolDepto, on_delete = models.CASCADE, db_column = 'id_rol')
		empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE, db_column = 'id_empresa')

		class Meta:
			db_table = 'departamento'

		def __str__(self):
			return self.nombre_depto

	class Funcion(models.Model):
		id_funcion = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 30)
		descripcion = models.CharField(max_length = 100)
		depto = models.ForeignKey(Departamento, on_delete = models.CASCADE, db_column = 'id_depto')

		class Meta:
			db_table = 'funcion'

		def __str__(self):
			return self.nombre

	class Tarea(models.Model):
		id_tarea = models.AutoField(primary_key = True)
		nombre = models.CharField(max_length = 30)
		descripcion = models.CharField(max_length = 100)
		fecha_inicio = models.DateField()
		fecha_termino = models.DateField(null = True, blank = True)
		fecha_plazo = models.DateField()
		duracion_dias = models.IntegerField()
		estado = models.ForeignKey(EstadoTarea, on_delete = models.CASCADE, db_column = 'id_estado')
		responsables = models.ManyToManyField(Funcionario, through = 'ResponsableTarea')

		class Meta:
			db_table = 'tarea'

		def __str__(self):
			return self.descripcion

	class ResponsableTarea(models.Model):
		funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE, db_column = 'id_funcionario')
		tarea = models.ForeignKey(Tarea, on_delete = models.CASCADE, db_column = 'id_tarea')
		justificativo = models.CharField(max_length = 50, null = True, blank = True)
		plazo_dias = models.IntegerField()

		class Meta:
			db_table = 'responsable_tarea'
			constraints = [
				models.UniqueConstraint(name = 'funcionario_tarea_un', fields = ('funcionario', 'tarea'))
			]

	class Problema(models.Model):
		id_problema = models.AutoField(primary_key = True)
		descripcion = models.CharField(max_length = 500)
		estado = models.CharField(max_length = 15)
		solucion_planteada = models.CharField(max_length = 500),
		funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE)
		tarea = models.ForeignKey(Tarea, on_delete = models.CASCADE)

		class Meta:
			db_table = 'problema'

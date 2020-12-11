from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime, timedelta
from .forms import *
from api.models import *

# Create your views here.
class PrincipalView(View):
	template_name = 'principal.html'
	context = {'title': 'Principal'}

	def get(self, request):
		return render(request, self.template_name, self.context)

class PanelView(LoginRequiredMixin, View):
	template_name = 'panel.html'
	context = {'title': 'Panel'}

	def get(self, request):
		funcionario = Funcionario.objects.get(email = request.user.username)
		self.context['funcionario'] = funcionario
		return render(request, self.template_name, self.context)

class CrearTareaView(LoginRequiredMixin, View):
	template_name = 'crear_tarea.html'
	form = CrearTareaForm
	context = {'title': 'Inicio de sesión', 'fail': False}

	def get(self, request):
		funcionario_obj = Funcionario.objects.get(usuario = request.user)
		self.context['form'] = self.form(empresa_pk = funcionario_obj.empresa.pk)
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = self.form(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Tarea.objects.create(
				nombre = data.get('nombre'),
				descripcion = data.get('descripcion'),
				fecha_plazo = data.get('fecha_plazo'),
				estado = EstadoTarea.objects.get(pk = 1),
				funcion = data.get('funcion'))
			return redirect('crear-tarea')
		return render(request, self.template_name, self.context)

class MenuAsignacionTareasView(LoginRequiredMixin, View):
	template_name = 'menu_asignar_tareas.html'
	context = {'title': 'Asignación de Tareas'}

	def get(self, request):
		funcionario_obj = Funcionario.objects.get(usuario = request.user)
		tareas = Tarea.objects.filter(estado__pk__lt = 6, funcion__depto__empresa = funcionario_obj.empresa)
		self.context['tareas'] = tareas
		return render(request, self.template_name, self.context)

class ListaResponsableView(LoginRequiredMixin, View):
	template_name = 'lista_responsables.html'
	context = {'title': 'Asignar Responsable'}

	def get(self, request, tarea):
		funcionario_obj = Funcionario.objects.get(usuario = request.user)
		tarea_obj = Tarea.objects.get(pk = tarea)
		funcionarios = Funcionario.objects.filter(empresa = funcionario_obj.empresa).exclude(pk__in = ResponsableTarea.objects.filter(tarea = tarea).values('funcionario'))
		self.context['tarea'] = tarea_obj
		self.context['funcionarios'] = funcionarios
		return render(request, self.template_name, self.context)

def asignar_responsable(request, tarea, responsable):
	asignador = Funcionario.objects.get(usuario = request.user)
	funcionario_obj = Funcionario.objects.get(pk = responsable)
	tarea_obj = Tarea.objects.get(pk = tarea)
	ResponsableTarea.objects.create(
		funcionario = funcionario_obj,
		tarea = tarea_obj,
		asignado_por = asignador.pk)
	if tarea_obj.estado.pk == 1:
		tarea_obj.estado = EstadoTarea.objects.get(pk = 2)
		tarea_obj.save()
	Notificacion.objects.create(
		contenido = 'Te han asignado la tarea ' + tarea_obj.nombre,
		funcionario = funcionario_obj)
	return redirect('lista-responsable', tarea)

class MisTareasView(LoginRequiredMixin, View):
	template_name = 'mis_tareas.html'
	context = {'title': 'Mis Tareas'}

	def get(self, request):
		hoy = datetime.now().date()
		funcionario_obj = Funcionario.objects.get(usuario = request.user)
		tareas = Tarea.objects.filter(responsables = funcionario_obj)
		arr_tareas = {}
		for t in tareas:
			# Determina la diferencia de días en que se encuentra la tarea frente al plazo
			if t.estado.pk != 6:
				dias = (t.fecha_plazo - hoy).days
			else:
				dias = (t.fecha_plazo - t.fecha_termino).days

			# Indicador del semáforo
			if dias > 7:
				semaforo = 3
			elif dias > 0:
				semaforo = 2
			else:
				semaforo = 1

			arr_tareas[str(t.pk)] = {'tarea': t, 'dias': dias, 'semaforo': semaforo}

		self.context['tareas'] = arr_tareas
		return render(request, self.template_name, self.context)

def ejecutar_tarea(request, tarea):
	tarea_obj = Tarea.objects.get(pk = tarea)
	tarea_obj.fecha_inicio = datetime.now()
	tarea_obj.estado = EstadoTarea.objects.get(pk = 3)
	tarea_obj.save()
	return redirect('mis-tareas')

def terminar_tarea(request, tarea):
	tarea_obj = Tarea.objects.get(pk = tarea)
	tarea_obj.fecha_termino = datetime.now()
	tarea_obj.estado = EstadoTarea.objects.get(pk = 6)
	tarea_obj.save()
	return redirect('mis-tareas')

class ReportarProblemaView(LoginRequiredMixin, View):
	template_name = 'report-problema.html'
	form = ReportarProblemaForm
	context = {'title': 'Reportar problema'}

	def get(self, request, tarea):
		self.context['form'] = self.form()
		return render(request, self.template_name, self.context)

	def post(self, request, tarea):
		form = self.form(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			funcionario_obj = Funcionario.objects.get(usuario = request.user)
			tarea_obj = Tarea.objects.get(pk = tarea)
			asignacion = ResponsableTarea(tarea = tarea_obj, funcionario = funcionario_obj)
			asignador = Funcionario.objects.get(pk = asignacion.asignado_por)
			Problema.objects.create(
				descripcion = data.get('descripcion'),
				estado = 'INGRESADO',
				funcionario = funcionario_obj,
				tarea = tarea_obj)
			Notificacion.objects.create(
				contenido = 'El funcionario ' + funcionario_obj + ' ha ingresado un problema para la tarea ' + tarea_obj,
				funcionario = asignador)
			return redirect('mis-tareas')
		return render(request, self.template_name, self.context)

class DevolverTareaView(LoginRequiredMixin, View):
	template_name = 'devolver_tarea.html'
	form = DevolverTareaForm
	context = {'title': 'Devolver tarea'}

	def get(self, request, tarea):
		self.context['form'] = self.form()
		return render(request, self.template_name, self.context)

	def post(self, request, tarea):
		form = self.form(request.POST, request.FILES or None)
		if form.is_valid():
			data = form.cleaned_data
			funcionario_obj = Funcionario.objects.get(usuario = request.user)
			tarea_obj = Tarea.objects.get(pk = tarea)
			asignacion = ResponsableTarea.objects.get(funcionario = funcionario_obj, tarea = tarea_obj)
			asignador = Funcionario.objects.get(pk = asignacion.asignado_por)
			Justificativo.objects.create(
				motivo = data.get('motivo'),
				documento = data.get('documento'),
				funcionario = funcionario_obj,
				tarea = tarea_obj)
			Notificacion.objects.create(
				contenido = 'El funcionario ' + funcionario_obj + 'ha ingresado una solicitud de devolución para la tarea ' + tarea_obj,
				funcionario = asignador)
			return redirect('mis-tareas')
		return render(request, self.template_name, self.context)

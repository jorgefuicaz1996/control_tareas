from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime, timedelta
from .forms import *
from django.db.models import Q
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
		self.context['form'] = self.form()
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = self.form(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			Tarea.objects.create(
				nombre = data.get('nombre'),
				descripcion = data.get('descripcion'),
				fecha_inicio = data.get('fecha_inicio'),
				fecha_plazo = data.get('fecha_plazo'),
				estado = EstadoTarea.objects.get(descripcion = 'Creada'),
				funcion = data.get('funcion'))
			return redirect('crear-tarea')
		return render(request, self.template_name, self.context)

class MenuAsignacionTareasView(LoginRequiredMixin, View):
	template_name = 'menu_asignar_tareas.html'
	context = {'title': 'Asignación de Tareas'}

	def get(self, request):
		tareas = Tarea.objects.all()
		self.context['tareas'] = tareas
		return render(request, self.template_name, self.context)

class ListaResponsableView(LoginRequiredMixin, View):
	template_name = 'lista_responsables.html'
	context = {'title': 'Asignar Responsable'}

	def get(self, request, tarea):
		tarea = Tarea.objects.get(pk = tarea)
		funcionarios = Funcionario.objects.exclude(pk__in = ResponsableTarea.objects.filter(tarea = tarea).values('funcionario'))
		self.context['tarea'] = tarea
		self.context['funcionarios'] = funcionarios
		return render(request, self.template_name, self.context)

def asignar_responsable(request, tarea, responsable):
	funcionario_obj = Funcionario.objects.get(pk = responsable)
	tarea_obj = Tarea.objects.get(pk = tarea)
	ResponsableTarea.objects.create(funcionario = funcionario_obj, tarea = tarea_obj)
	if tarea_obj.estado != 'Asignada':
		tarea_obj.estado = EstadoTarea.objects.get(descripcion = 'Asignada')
		tarea_obj.save()
	return redirect('lista-responsable', tarea)

class MisTareasView(LoginRequiredMixin, View):
	template_name = 'mis_tareas.html'
	context = {'title': 'Mis Tareas'}

	def get(self, request):
		hoy = datetime.now().date()
		funcionario = Funcionario.objects.get(email = request.user.username)
		tareas = Tarea.objects.filter(responsables = funcionario)
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
			Problema.objects.create(
				descripcion = data.get('descripcion'),
				estado = 'INGRESADO',
				funcionario = funcionario_obj,
				tarea = tarea_obj)
			return redirect('mis-tareas')
		return render(request, self.template_name, self.context)

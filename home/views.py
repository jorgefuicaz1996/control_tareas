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

class Crear_tareaView(LoginRequiredMixin, View):
	template_name = 'crear_tarea.html'
	form = CrearTareaForm()
	context = {'title': 'Inicio de sesión', 'form': form, 'fail': False}

	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		self.form = CrearTareaForm(request.POST)
		if self.form.is_valid():
			data = self.form.cleaned_data
			Tarea.objects.create(
				nombre = data.get('nombre'),
				descripcion = data.get('descripcion'),
				fecha_inicio = data.get('fecha_inicio'),
				fecha_plazo = data.get('fecha_inicio') + timedelta(days = data.get('duracion_dias')),
				duracion_dias = data.get('duracion_dias'),
				estado = EstadoTarea.objects.get(descripcion = 'Creada')
			)
			return redirect('crear-tarea')
		return render(request, self.template_name, self.context)

class MenuAsignacionTareasView(View):
	template_name = 'menu_asignar_tareas.html'
	context = {'title': 'Asignación de Tareas'}

	def get(self, request):
		tareas = Tarea.objects.all()
		self.context['tareas'] = tareas
		return render(request, self.template_name, self.context)

class ListaResponsableView(View):
	template_name = 'lista_responsables.html'
	context = {'title': 'Asignar Responsable'}

	def get(self, request, tarea):
		tarea = Tarea.objects.get(pk = tarea)
		funcionarios = Funcionario.objects.exclude(pk__in = ResponsableTarea.objects.filter(tarea = tarea).values('funcionario'))
		form = AsignarResponsableForm()
		self.context['tarea'] = tarea
		self.context['funcionarios'] = funcionarios
		self.context['form'] = form
		return render(request, self.template_name, self.context)

def asignar_responsable(request, tarea, responsable):
	form = AsignarResponsableForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		funcionario_obj = Funcionario.objects.get(pk = responsable)
		tarea_obj = Tarea.objects.get(pk = tarea)
		ResponsableTarea.objects.create(funcionario = funcionario_obj, tarea = tarea_obj, plazo_dias = data.get('plazo_dias'))
		if tarea_obj.estado != 'Asignada':
			tarea_obj.estado = EstadoTarea.objects.get(descripcion = 'Asignada')
			tarea_obj.save()
		return redirect('lista-responsable', tarea)

class MisTareasView(View):
	template_name = 'mis_tareas.html'
	context = {'title': 'Mis Tareas'}

	def get(self, request):
		funcionario = Funcionario.objects.get(email = request.user.username)
		tareas = Tarea.objects.filter(responsables = funcionario)
		self.context['tareas'] = tareas
		return render(request, self.template_name, self.context)


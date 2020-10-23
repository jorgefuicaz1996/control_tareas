from django.shortcuts import render
from django.views import View
from .forms import *

# Create your views here.
class PrincipalView(View):
	template_name = 'principal.html'
	context = {'title': 'Principal'}

	def get(self, request):
		return render(request, self.template_name, self.context)

class PanelView(View):
	template_name = 'panel.html'
	context = {'title': 'Panel'}

	def get(self, request):
		return render(request, self.template_name, self.context)
		
class Crear_tareaView(View):
	template_name = 'crear_tarea.html'
	form = Crear_tareaForm()
	context = {'title': 'Inicio de sesión', 'form': form, 'fail': False}

	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		self.form = Crear_tareaForm(request.POST)
		if self.form.is_valid():
			return render(request, self.template_name, self.context)
		return render(request, self.template_name, self.context)
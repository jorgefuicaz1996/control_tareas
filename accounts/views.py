from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from .forms import *

# Create your views here.
class LoginView(View):
	template_name = 'login.html'
	form = LoginForm()
	context = {'title': 'Inicio de sesión', 'form': form, 'fail': False}

	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		self.form = LoginForm(request.POST)
		if self.form.is_valid():
			data = self.form.cleaned_data
			user = authenticate(username = data.get('username'), password = data.get('password'))
			if user:
				login(request, user)
				return redirect('/')
			self.context['fail'] = True
		return render(request, self.template_name, self.context)

def cerrar_sesion(request):
	logout(request)
	return redirect('/')

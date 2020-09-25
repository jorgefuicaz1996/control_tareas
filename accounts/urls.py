from django.urls import path
from . import views

urlpatterns = [
	path('login', views.LoginView.as_view(), name = 'log-in'),
	path('logout', views.cerrar_sesion, name = 'log-out'),
]

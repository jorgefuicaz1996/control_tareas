from django.urls import path
from . import views

urlpatterns = [
	path('', views.PrincipalView.as_view(), name = 'principal'),
	path('panel', views.PanelView.as_view(), name = 'panel'),
	path('crear-tarea', views.Crear_tareaView.as_view(), name = 'crear-tarea'),
]

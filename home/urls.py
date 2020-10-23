from django.urls import path
from . import views

urlpatterns = [
	path('', views.PrincipalView.as_view(), name = 'principal'),
	path('panel', views.PanelView.as_view(), name = 'panel'),
	path('crear-tarea', views.Crear_tareaView.as_view(), name = 'crear-tarea'),
	path('asignar-tarea', views.MenuAsignacionTareasView.as_view(), name = 'menu-asignar-tarea'),
	path('asignar-tarea/<int:tarea>', views.ListaResponsableView.as_view(), name = 'lista-responsable'),
	path('asignar-tarea/<int:tarea>/<int:responsable>', views.asignar_responsable, name = 'asignar-responsable'),
	path('mistareas', views.MisTareasView.as_view(), name = 'mis-tareas'),
]

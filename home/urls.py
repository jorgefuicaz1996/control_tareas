from django.urls import path
from . import views

urlpatterns = [
	path('', views.PrincipalView.as_view(), name = 'principal'),
	path('panel', views.PanelView.as_view(), name = 'panel'),
	path('crear-tarea', views.CrearTareaView.as_view(), name = 'crear-tarea'),
	path('asignar-tarea', views.MenuAsignacionTareasView.as_view(), name = 'menu-asignar-tarea'),
	path('asignar-tarea/<int:tarea>', views.ListaResponsableView.as_view(), name = 'lista-responsable'),
	path('asignar-tarea/<int:tarea>/<int:responsable>', views.asignar_responsable, name = 'asignar-responsable'),
	path('mis-tareas', views.MisTareasView.as_view(), name = 'mis-tareas'),
	path('mis-tareas/reportar-problema/<int:tarea>', views.ReportarProblemaView.as_view(), name = 'reportar-problema'),
	path('mis-tareas/devolver/<int:tarea>', views.DevolverTareaView.as_view(), name = 'devolver-tarea'),
	path('mis-tareas/ejecutar/<int:tarea>', views.ejecutar_tarea, name = 'ejecutar-tarea'),
	path('mis-tareas/terminar/<int:tarea>', views.terminar_tarea, name = 'terminar-tarea'),
]

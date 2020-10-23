from django import forms
from datetime import datetime

class Crear_tareaForm(forms.Form):
	nombre = forms.CharField(
		label = 'Nombre de tarea',
		widget = forms.TextInput(attrs = {'id': 'nombre', 'placeholder': 'Ingrese el nombre de la tarea'})
	)
	fecha_inicio = forms.DateField(
		label = 'Fecha de inicio de la tarea',
		widget = forms.SelectDateWidget(years=range(datetime.now().year,datetime.now().year+10))
	)
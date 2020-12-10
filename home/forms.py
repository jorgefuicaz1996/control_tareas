from django import forms
from datetime import datetime
from api.models import Funcion, Tarea

class CrearTareaForm(forms.Form):
	nombre = forms.CharField(
		max_length = 30,
		widget = forms.TextInput())

	descripcion = forms.CharField(
		label = 'Descripción',
		max_length = 100,
		widget = forms.Textarea())

	fecha_inicio = forms.DateField(
		widget = forms.SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 10)))

	fecha_plazo = forms.DateField(
		widget = forms.SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 10)))

	funcion = forms.ModelChoiceField(
		label = 'Función asociada',
		queryset = Funcion.objects.all())

class ReportarProblemaForm(forms.Form):
	descripcion = forms.CharField(
		label = 'Descripción',
		max_length = 500,
		widget = forms.Textarea())

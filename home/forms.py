from django import forms
from datetime import datetime

class CrearTareaForm(forms.Form):
	descripcion = forms.CharField(
		label = 'Descripción',
		widget = forms.TextInput(attrs = {'id': 'descripcion', 'placeholder': 'Ingrese descripción'})
	)

	fecha_inicio = forms.DateField(
		label = 'Fecha inicio',
		widget = forms.SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 10))
	)

	duracion_dias = forms.IntegerField(
		label = 'Duración en días',
		widget = forms.NumberInput(attrs = {'id': 'duracion_dias'}),
		min_value = 1,
		initial = 1
	)

class AsignarResponsableForm(forms.Form):
	plazo_dias = forms.IntegerField(
		label = 'Plazo en días',
		widget = forms.NumberInput(),
		min_value = 1,
		initial = 1
	)

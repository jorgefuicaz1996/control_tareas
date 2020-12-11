from django import forms
from datetime import datetime
from api.models import Funcion, Empresa, Tarea

class CrearTareaForm(forms.Form):
	nombre = forms.CharField(
		max_length = 30,
		widget = forms.TextInput())

	descripcion = forms.CharField(
		label = 'Descripción',
		max_length = 100,
		widget = forms.Textarea())

	fecha_plazo = forms.DateField(
		widget = forms.SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 10)))

	funcion = forms.ModelChoiceField(
		label = 'Función asociada',
		queryset = Funcion.objects.all())

	def __init__(self, *args, **kwargs):
		if 'empresa_pk' in kwargs:
			empresa = Empresa.objects.get(pk = int(kwargs.pop('empresa_pk')))
			super().__init__(*args, **kwargs)
			self.fields['funcion'].queryset = Funcion.objects.filter(depto__empresa = empresa)
		else:
			super().__init__(*args, **kwargs)

class ReportarProblemaForm(forms.Form):
	descripcion = forms.CharField(
		label = 'Descripción',
		max_length = 500,
		widget = forms.Textarea())

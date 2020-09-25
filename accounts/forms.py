from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(
		label = 'Nombre de usuario',
		widget = forms.TextInput(attrs = {'id': 'username', 'placeholder': 'Ingrese nombre de usuario'})
	)

	password = forms.CharField(
		label = 'Contraseña',
		widget = forms.PasswordInput(attrs = {'id': 'password', 'placeholder': 'Ingrese contraseña'})
	)

from django import forms
from django.core.validators import RegexValidator

class inicioSesion(forms.Form):

	email = forms.EmailField(label="Email", 
		widget=forms.TextInput(attrs={"placeholder" : "Email", "class": "form-control"}), 
		required=True)
	passwd = forms.CharField(label="Contraseña", 
		widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
		min_length=8, 
		required=True)
 
class registro(forms.Form):
    
	nombre = forms.CharField(label="Nombre", 
		widget=forms.TextInput(attrs={"placeholder" : "Nombre", "class": "form-control"}),
		required=True)
	apellidos = forms.CharField(label="Apellidos", 
		widget=forms.TextInput(attrs={"placeholder" : "Apellidos", "class": "form-control"}), 
		 required=True)
 
	passwd = forms.CharField(label="Contraseña", 
		widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
		min_length=8, 
		required=True)
	repeatPasswd = forms.CharField(label="Repetir contraseña", 
		widget=forms.PasswordInput(attrs={"placeholder" : "Repetir contraseña","class": "form-control"}), 
		min_length=8,required=True)
 
	nacimiento = forms.DateField(
		label="Fecha de Nacimiento",
		input_formats='%d-%m-%Y',
		widget=forms.DateInput(attrs={"placeholder" : "dd/mm/YYYY", "class": "form-control datepicker"}),
		required=True)
 
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
		message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	movil = forms.CharField(validators=[phone_regex], 
		widget=forms.TextInput(attrs={"placeholder" : "Telefono movil","class": "form-control"}), 
		max_length=17)

	email = forms.EmailField(label="Email", 
		widget=forms.TextInput(attrs={"placeholder" : "Email","class": "form-control"}), 
		required=True)
    
    
    
    
    
    
    
    

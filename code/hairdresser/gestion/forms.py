from django import forms
from django.db.models import Q
from .models import *
from django.core.validators import RegexValidator

def positive_validator(value):
    if value < 0:
        raise forms.ValidationError("El valor debe ser positivo.")

class PositiveIntegerField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.get("validators", [])
        validators.append(positive_validator)
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)

class crearServicioForm(forms.ModelForm):

	nombre = forms.CharField(label="Nombre", 
		widget=forms.TextInput(attrs={"placeholder" : "Servicio", "class": "form-control"}),
		required=True)
	precio = forms.FloatField(label="Precio", 
		widget=forms.NumberInput(attrs={"placeholder" : "Precio","class": "form-control", "min" : "1", "suffix": "€"}), 
		required=True)
	duracion = PositiveIntegerField(label="Duración", 
		widget=forms.NumberInput(attrs={"placeholder" : "Duración","class": "form-control", "step": "1", "min" : "1", "suffix": "minutos"}), 
		required=True)
	ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.all(),
        empty_label="",
        required=False)
	oferta = forms.ModelChoiceField(queryset=Oferta.objects.all(),
        empty_label="",
        required=False)
	descripcion = forms.CharField(label="Descripcion",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False)
	activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
 
	fields = ['nombre', 'precio', 'duracion', 'ubicacion', 'oferta', 'descripcion', 'activo']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ubicacion'].widget.attrs['class'] = 'form-control'
		self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicacion'
		self.fields['oferta'].widget.attrs['class'] = 'form-control'
		self.fields['oferta'].widget.attrs['placeholder'] = 'Oferta'

	class Meta:
		model = Servicio
		fields = '__all__'

class modificarServicioForm(forms.ModelForm):

	id= forms.CharField(widget=forms.HiddenInput)
	nombre = forms.CharField(label="Nombre", 
		widget=forms.TextInput(attrs={"placeholder" : "Servicio", "class": "form-control"}),
		required=True)
	precio = forms.FloatField(label="Precio", 
		widget=forms.NumberInput(attrs={"placeholder" : "Precio","class": "form-control", "min" : "1", "suffix": "€"}), 
		required=True)
	duracion = PositiveIntegerField(label="Duración", 
		widget=forms.NumberInput(attrs={"placeholder" : "Duración","class": "form-control", "step": "1", "min" : "1", "suffix": "minutos"}), 
		required=True)
	ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.values_list('nombre', flat=True),
        empty_label="",
        required=False)
	oferta = forms.ModelChoiceField(queryset=Oferta.objects.values_list('nombre', flat=True),
        empty_label="",
        required=False)
	descripcion = forms.CharField(label="Descripcion",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False)
	activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
 
	fields = ['id', 'nombre', 'precio', 'duracion', 'ubicacion', 'oferta', 'descripcion', 'activo']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# ubicaciones = Ubicacion.objects.values_list("nombre", flat=True)
		# choices = [(nombre, nombre) for nombre in ubicaciones]
		self.fields['id'].label = ''
		self.fields['ubicacion'].widget.attrs['class'] = 'form-control'
		self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicacion'
		self.fields['oferta'].widget.attrs['class'] = 'form-control'
		self.fields['oferta'].widget.attrs['placeholder'] = 'Oferta'
 
	class Meta:
		model = Servicio
		fields = '__all__'

class crearOfertaForm(forms.ModelForm):

	nombre = forms.CharField(label="Oferta", 
		widget=forms.TextInput(attrs={"placeholder" : "Oferta", "class": "form-control"}),
		required=True)
	descuento = forms.FloatField(label="Descuento", 
		widget=forms.NumberInput(attrs={"placeholder" : "Descuento","class": "form-control", "min" : "0", "suffix": "€"}), 
		required=True)
	fecha_fin = forms.DateField(
		label="Fecha Fin",
		input_formats='%d-%m-%Y',
		widget=forms.DateInput(attrs={"placeholder" : "dd/mm/YYYY", "class": "form-control datepicker"}),
		required=False)
	activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
 
	fields = ['nombre', 'descuento', 'fecha_fin''activo']


class crearCitaForm(forms.ModelForm):

	servicio = forms.ModelChoiceField(queryset=Servicio.objects.filter(Q(activo='1')),
        empty_label="",
        required=False)
	cliente = forms.ModelChoiceField(queryset=Usuario.objects.filter(Q(role_id='3') & Q(activo='1')),
        empty_label="",
        required=False)	
	fecha_cita = forms.DateField(
		label="Fecha cita",
		input_formats='%d-%m-%Y',
		widget=forms.DateInput(attrs={"placeholder" : "dd/mm/YYYY", "class": "form-control datepicker"}),
		required=True)
 
	class Meta:
		model = Cita
		fields = '__all__'

class modificarOfertaForm(crearOfertaForm):
    
	id= forms.CharField(widget=forms.HiddenInput)
    
	fields = ['id','nombre', 'descuento', 'fecha_fin''activo']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['id'].label = ''
  
	class Meta:
		model = Oferta
		fields = '__all__'
   
class crearUsuarioForm(forms.ModelForm):

	nombre = forms.CharField(label="Nombre", 
		widget=forms.TextInput(attrs={"placeholder" : "Nombre", "class": "form-control"}),
		required=True)
	apellidos = forms.CharField(label="Apellidos", 
		widget=forms.TextInput(attrs={"placeholder" : "Apellidos", "class": "form-control"}),
		required=True)
	fecha_nacimiento = forms.DateField(
		label="Fecha nacimiento",
		input_formats='%d-%m-%Y',
		widget=forms.DateInput(attrs={"placeholder" : "dd/mm/YYYY", "class": "form-control datepicker"}),
		required=True)
	passwd = forms.CharField(label="Contraseña", 
		widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
		min_length=8, 
		required=True)
	role = forms.ModelChoiceField(label="Rol", queryset=Roles.objects.all(),
        empty_label="",
        required=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
		message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") 
	movil = PhoneNumberField()
	email = forms.EmailField(label="Email", 
		widget=forms.TextInput(attrs={"placeholder" : "Email","class": "form-control"}), 
		required=True)
 
	fields = ['nombre', 'apellidos', 'passwd', 'email', 'movil', 'role', 'activo']
 
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['movil'].widget.attrs['class'] = 'form-control'
		self.fields['movil'].widget.attrs['placeholder'] = 'Movil'
		self.fields['role'].widget.attrs['class'] = 'form-control'
		self.fields['role'].widget.attrs['placeholder'] = 'Rol'
 
 
	class Meta:
		model = Usuario
		fields = '__all__'

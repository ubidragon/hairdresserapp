import re
from django import forms
from django.db.models import Q
from .models import *
from django.core.validators import RegexValidator

# Metodos y funcionalidades para los formularios
def positive_validator(value):
    if value < 0:
        raise forms.ValidationError("El valor debe ser positivo.")

class PositiveIntegerField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.get("validators", [])
        validators.append(positive_validator)
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)

class UsuarioCustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, instance):
        # Personaliza la representación del objeto en el ModelChoiceField
        return instance.nombre + " " + instance.apellidos
    
class OfertaCustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, instance):
        # Personaliza la representación del objeto en el ModelChoiceField
        return instance.nombre
# 
# 
# 
# Formularios de la aplicacion
# 

# SERVICIO
class crearServicioForm(forms.ModelForm):

  nombre = forms.CharField(label="Nombre", 
    widget=forms.TextInput(attrs={"placeholder" : "Servicio", "class": "form-control"}),
      min_length=1,
    required=True)
  precio = forms.FloatField(label="Precio", 
    widget=forms.NumberInput(attrs={"placeholder" : "Precio","class": "form-control", "min" : "1", "suffix": "€"}),
    min_value=1,
    required=True)
  duracion = PositiveIntegerField(label="Duración", 
    widget=forms.NumberInput(attrs={"placeholder" : "Duración","class": "form-control", "step": "1", "min" : "1", "suffix": "minutos"}), 
    required=True)
  ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.all(),
        empty_label="",
        required=True)
  oferta = forms.ModelChoiceField(queryset=Oferta.objects.all(),
        empty_label="",
        required=False)
  descripcion = forms.CharField(label="Descripcion",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False)
  activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['ubicacion'].widget.attrs['class'] = 'form-control'
    self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicacion'
    self.fields['oferta'].widget.attrs['class'] = 'form-control'
    self.fields['oferta'].widget.attrs['placeholder'] = 'Oferta'

  class Meta:
    model = Servicio
    fields = ['nombre', 'precio', 'duracion', 'ubicacion', 'oferta', 'descripcion', 'activo']

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
  oferta = OfertaCustomModelChoiceField(queryset=Oferta.objects.all(),
        empty_label="",
        required=False)
  descripcion = forms.CharField(label="Descripcion",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False)
  activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
    self.fields['ubicacion'].widget.attrs['class'] = 'form-control'
    self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicacion'
    self.fields['oferta'].widget.attrs['class'] = 'form-control'
    self.fields['oferta'].widget.attrs['placeholder'] = 'Oferta'
 
  class Meta:
    model = Servicio
    fields = ['id', 'nombre', 'precio', 'duracion', 'ubicacion', 'oferta', 'descripcion', 'activo']

# OFERTA
class crearOfertaForm(forms.ModelForm):

  nombre = forms.CharField(label="Oferta", 
    widget=forms.TextInput(attrs={"placeholder" : "Oferta", "class": "form-control"}),
      min_length=1,
    required=True)
  descuento = forms.FloatField(label="Descuento", 
    widget=forms.NumberInput(attrs={"placeholder" : "Descuento","class": "form-control", "min" : "0", "suffix": "€"}),
    min_value=0,
    required=True)
  fecha_fin = forms.DateField(
    label="Fecha Fin",
    input_formats=['%Y-%m-%d'],
    widget=forms.DateInput(attrs={"placeholder" : "YYYY-mm-dd", "class": "form-control datepicker"}),
    required=False)
  activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
 
  class Meta:
    model = Oferta
    fields = ['nombre', 'descuento', 'fecha_fin','activo']
   
class modificarOfertaForm(crearOfertaForm):

  id= forms.CharField(widget=forms.HiddenInput)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
  
  class Meta:
    model = Oferta
    fields = ['id','nombre', 'descuento', 'fecha_fin','activo']

# CITA
class crearCitaAdminForm(forms.ModelForm):
  servicio = forms.ModelChoiceField(queryset=Servicio.objects.filter(Q(activo='1')),
        empty_label="",
        required=True)

  cliente = UsuarioCustomModelChoiceField(queryset=Usuario.objects.filter(Q(role_id='3') & Q(activo='1')),
        required=True)

  empleado = UsuarioCustomModelChoiceField(queryset=Usuario.objects.filter(Q(role_id='2') & Q(activo='1')),
    required=True)	

  fecha_cita = forms.DateField(
    label="Fecha cita",
    input_formats=['%Y-%m-%d'],
    widget=forms.DateInput(attrs={"placeholder" : "YYYY-mm-dd", "class": "form-control datepicker"}),
    required=True)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['cliente'].widget.attrs['class'] = 'form-control'
    self.fields['cliente'].widget.attrs['placeholder'] = 'Cliente'
    self.fields['empleado'].widget.attrs['class'] = 'form-control'
    self.fields['empleado'].widget.attrs['placeholder'] = 'Empleado'
    self.fields['servicio'].widget.attrs['class'] = 'form-control'
    self.fields['servicio'].widget.attrs['placeholder'] = 'Servicio'

  class Meta:
    model = Cita
    fields = ['servicio', 'cliente', 'empleado', 'fecha_cita', ]
  
class crearCitaClienteForm(crearCitaAdminForm):

  cliente = forms.CharField(widget=forms.HiddenInput)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['cliente'].label = ''
 
  class Meta:
    model = Cita
    fields = ['servicio', 'fecha_cita']

class modificarCitaForm(crearCitaAdminForm):

  id= forms.CharField(widget=forms.HiddenInput)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
  
  class Meta:
    model = Cita
    fields = ['servicio', 'cliente', 'empleado', 'fecha_cita', ]

class modificarCitaClienteForm(crearCitaAdminForm):

  id= forms.CharField(widget=forms.HiddenInput)
  cliente = forms.CharField(widget=forms.HiddenInput)
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
    self.fields['cliente'].label = ''
  
  class Meta:
    model = Cita
    fields = ['servicio', 'empleado', 'fecha_cita', ]
  
class modificarCitaPasada(modificarCitaForm):

  fecha_cita = forms.CharField()

  def __init__(self, *args, **kwargs):
    super(crearCitaAdminForm, self).__init__(*args, **kwargs)
    self.fields['id'].label = ''
    self.fields['servicio'].widget.attrs['disabled'] = True
    self.fields['cliente'].widget.attrs['disabled'] = True
    self.fields['empleado'].widget.attrs['disabled'] = True
    self.fields['fecha_cita'].widget.attrs['readonly'] = True
  
  class Meta:
    model = Cita
    fields = ['servicio', 'cliente', 'empleado', 'fecha_cita', ]

# USUARIO
class crearUsuarioForm(forms.ModelForm):

  nombre = forms.CharField(label="Nombre", 
    widget=forms.TextInput(attrs={"placeholder" : "Nombre", "class": "form-control"}),
      max_length=100,
    required=True)
  apellidos = forms.CharField(label="Apellidos", 
    widget=forms.TextInput(attrs={"placeholder" : "Apellidos", "class": "form-control"}),
    min_length=1,
    max_length=255,
    required=True)
  fecha_nacimiento = forms.DateField(
    label="Fecha nacimiento",
    input_formats=['%Y-%m-%d'],
    widget=forms.DateInput(attrs={"placeholder" : "YYYY-mm-dd", "class": "form-control datepicker"}),
    required=False)
  password = forms.CharField(label="Contraseña", 
    widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
    min_length=8,
    max_length=500,
    required=True)
  role = forms.ModelChoiceField(label="Rol", queryset=Roles.objects.all(),
        empty_label="",
        required=True)
  phone_regex = RegexValidator(
                regex=r'^\d{9}$',
                message='El número de teléfono móvil debe longitud de 9.'
            )
  movil = forms.CharField(validators=[phone_regex], required=False)

  email = forms.EmailField(label="Email", 
    widget=forms.TextInput(attrs={"placeholder" : "Email","class": "form-control"}),
    required=True)
 
  activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
  
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['movil'].widget.attrs['class'] = 'form-control'
    self.fields['movil'].widget.attrs['placeholder'] = 'Movil'
    self.fields['role'].widget.attrs['class'] = 'form-control'
    self.fields['role'].widget.attrs['placeholder'] = 'Rol'
  
  class Meta:
    model = Usuario
    fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'password', 'email', 'movil', 'role', 'activo']

class modificarUsuarioForm(forms.ModelForm):
  id= forms.CharField(widget=forms.HiddenInput)
  
  nombre = forms.CharField(label="Nombre", 
    widget=forms.TextInput(attrs={"placeholder" : "Nombre", "class": "form-control"}),
      max_length=100,
    required=True)
  apellidos = forms.CharField(label="Apellidos", 
    widget=forms.TextInput(attrs={"placeholder" : "Apellidos", "class": "form-control"}),
    min_length=1,
    max_length=255,
    required=True)
  fecha_nacimiento = forms.DateField(
    label="Fecha nacimiento",
    input_formats=['%Y-%m-%d'],
    widget=forms.DateInput(attrs={"placeholder" : "YYYY-mm-dd", "class": "form-control datepicker"}),
    required=False)
  password = forms.CharField(label="Contraseña", 
    widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
    min_length=8,
    max_length=500,
    required=True)
  role = forms.ModelChoiceField(label="Rol", queryset=Roles.objects.all(),
        empty_label="",
        required=True)
  phone_regex = RegexValidator(
                regex=r'^\d{9}$',
                message='El número de teléfono móvil debe longitud de 9.'
            )
  movil = forms.CharField(validators=[phone_regex], required=False)
 
  activo = forms.BooleanField(label="Activo",
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
        required=False)
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
    self.fields['movil'].widget.attrs['class'] = 'form-control'
    self.fields['movil'].widget.attrs['placeholder'] = 'Movil'
    self.fields['role'].widget.attrs['class'] = 'form-control'
    self.fields['role'].widget.attrs['placeholder'] = 'Rol'

  class Meta:
    model = Usuario
    fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'password', 'movil', 'role', 'activo']



class misDatosForm(forms.ModelForm):
  id= forms.CharField(widget=forms.HiddenInput)
  
  nombre = forms.CharField(label="Nombre", 
    widget=forms.TextInput(attrs={"placeholder" : "Nombre", "class": "form-control"}),
      max_length=100,
    required=True)
  apellidos = forms.CharField(label="Apellidos", 
    widget=forms.TextInput(attrs={"placeholder" : "Apellidos", "class": "form-control"}),
    min_length=1,
    max_length=255,
    required=True)
  fecha_nacimiento = forms.DateField(
    label="Fecha nacimiento",
    input_formats=['%Y-%m-%d'],
    widget=forms.DateInput(attrs={"placeholder" : "YYYY-mm-dd", "class": "form-control datepicker"}),
    required=False)
  password = forms.CharField(label="Contraseña", 
    widget=forms.PasswordInput(attrs={"placeholder" : "Contraseña","class": "form-control"}), 
    min_length=8,
    max_length=500,
    required=True)
  phone_regex = RegexValidator(
                regex=r'^\d{9}$',
                message='El número de teléfono móvil debe longitud de 9.'
            )
  movil = forms.CharField(validators=[phone_regex], required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['id'].label = ''
    self.fields['movil'].widget.attrs['class'] = 'form-control'
    self.fields['movil'].widget.attrs['placeholder'] = 'Movil'

  class Meta:
    model = Usuario
    fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'password', 'movil']
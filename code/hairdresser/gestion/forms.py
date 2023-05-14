from django import forms
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
	ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.values_list("nombre", flat=True),
        empty_label="",
        initial="",
        required=False)
	oferta = forms.ModelChoiceField(queryset=Oferta.objects.values_list("nombre", flat=True),
        empty_label="",
        required=False)
	descripcion = forms.CharField(label="Descripcion",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False)
 
	fields = ['nombre', 'precio', 'duracion', 'ubicacion', 'oferta', 'descripcion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		ubicaciones = Ubicacion.objects.values_list("nombre", flat=True)
		choices = [(nombre, nombre) for nombre in ubicaciones]
		self.fields['ubicacion'].widget.attrs['class'] = 'form-control'
		self.fields['ubicacion'].widget.attrs['placeholder'] = 'Ubicacion'
		self.fields['oferta'].widget.attrs['class'] = 'form-control'
		self.fields['oferta'].widget.attrs['placeholder'] = 'Oferta'

 
	class Meta:
		model = Servicio
		fields = '__all__'

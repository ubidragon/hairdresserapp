from django import forms

class FormularioContacto(forms.Form):
    
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    mensaje =  forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={"class": "form-control"}), required=True)
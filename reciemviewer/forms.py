# Red Ciudadana de Estaciones Meteorologicas
# All rights reserved 2019
#
# GIS online system
# Santiago Nunez-Corrales <snunezcr@gmail.com>

from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Correo electrónico', required=True)
    name = forms.CharField(label='Nombre', required=True)
    subject = forms.CharField(label='Asunto', required=True)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea, required=True)

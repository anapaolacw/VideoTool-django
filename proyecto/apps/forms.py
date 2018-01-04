from django import forms
from django.core.validators import FileExtensionValidator
from .models import Video
from django.db import models
from django.forms import TextInput, Textarea, FileInput

class VideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super (VideoForm, self).__init__(*args, **kwargs)
		#Propiedades de los campos
        self.fields['titulo'].required = True
        self.fields['titulo'].max_length = 50
        self.fields['titulo'].error_messages = {'required': "Campo obligatorio"}
    class Meta:
        model = Video
        fields = ('titulo', 'resumen', 'archivo')
        widgets = {
        	'titulo': TextInput(attrs={'class': 'form-control', 'novalidate':''}),
        	'resumen': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        	'archivo': FileInput(attrs={'class': 'form-control', 'accept':"video/mp4,video/x-m4v,video/*"}),
            'autor': TextInput(attrs={'placeholder': 'Autor'})
        }
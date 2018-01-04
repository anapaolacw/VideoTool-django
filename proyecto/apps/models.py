from django.db import models

# Create your models here.
class Usuario (models.Model):
	nombre = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	contrasena = models.CharField(max_length=50)
	correo = models.EmailField(max_length=70)

class Video (models.Model):
	titulo = models.CharField(max_length=50)
	resumen = models.TextField(null = True)
	archivo = models.FileField(upload_to='videos/')
	numeroVisto = models.IntegerField(default='0')
	numeroBuscado = models.IntegerField(default='0')
	fecha = models.DateTimeField(null = True, auto_now_add=True)
	autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

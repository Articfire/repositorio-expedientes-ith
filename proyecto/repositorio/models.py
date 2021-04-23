from django.db import models

# Create your models here.
class Alumno(models.Model):
    """docstring for Alumno.
        nombre_completo se compone de todos los nombres y apellidos del alumno.
        numero_control es el numero unico que identifica a cada alumno.
        carrera es que carrera eligio el alumno.
    """
    nombre_completo = models.CharField(max_length=50) # varchar(50)
    numero_control = models.IntegerField(default=0) # int
    carrera = models.CharField(max_length=50) # varchar(50)

class Archivo(models.Model):
    """docstring for Archivo.
        nombre significa nombre del archivo, excluyendo a la ruta y a la extension. Ej: acta de nacimiento
        ruta significa la ubicacion del archivo es. Ej: /home/martin/Desktop
        extension significa el tipo de archivo. Ej: .pdf, .docx, .xlsx, .exe
        pertenece_a es la llave foranea que apunta a la tabla ALumno, haciendo una conexion muchos a uno.
    """
    nombre = models.CharField(max_length=50) # varchar(50)
    ruta = models.CharField(max_length=100) # varchar(50)
    extension = models.CharField(max_length=5) # varchar(50)
    pertenece_a = models.ForeignKey(Alumno, on_delete=models.CASCADE) # int

class Usuario(models.Model):
    """docstring for Usuario."""

from django.db import models

# Create your models here.
class Alumno(models.Model):
    """docstring for Alumno.
        nombre_completo se compone de todos los nombres y apellidos del alumno.
        numero_control es el numero unico que identifica a cada alumno.
        carrera es que carrera eligio el alumno.
    """
    nombre_completo = models.CharField(max_length=50) # varchar(50)
    numero_control = models.IntegerField(default=0, unique = True) # int
    carrera = models.CharField(max_length=50) # varchar(50)

    def __str__(self):
        return self.nombre_completo

class Archivo(models.Model):
    """docstring for Archivo.
        nombre significa nombre del archivo, excluyendo a la ruta y a la extension. Ej: acta de nacimiento
        extension significa el tipo de archivo. Ej: .pdf, .docx, .xlsx, .exe
        pertenece_a es la llave foranea que apunta a la tabla Alumno, haciendo una conexion muchos a uno.
    """
    nombre = models.CharField(max_length=50) # varchar(50)
    extension = models.CharField(max_length=5) # varchar(50)
    pertenece_a = models.ForeignKey(Alumno, on_delete=models.CASCADE) # int

    def __str__(self):
        return "{}.{}".format(self.nombre, self.extension)

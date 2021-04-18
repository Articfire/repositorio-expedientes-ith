from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ControladorInicio(request):
    return HttpResponse("Inicio")

def ControladorImportarAlumnos(request):
    return HttpResponse("Importar Alumnos")

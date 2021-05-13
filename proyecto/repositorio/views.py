from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import pandas as pd

from .models import Alumno

# Create your views here.
def ControladorInicio(request):
    '''
    # render() es la manera mas facil de enviar html por una respuesta.
    # request es un objeto peticion con la informacion del navegador, etc.
    # template_name es un string con la ruta del template.
    '''
    return render(request, 'inicio.html')

def ControladorImportarAlumnos(request):
    '''docstring para ControladorImportarAlumnos.'''
    data = {'error': None}
    if request.method == 'POST':
        if request.FILES.get('archivo'):
            mi_archivo = request.FILES.get('archivo')
            fs = FileSystemStorage()
            nombre_archivo = fs.save(mi_archivo.name, mi_archivo)

            info_excel = pd.read_excel(r'media/{}'.format(mi_archivo.name))
            diccionario_alumnos = info_excel.to_dict('index')

            for fila in diccionario_alumnos.values():
                alumno_nuevo = Alumno(
                    nombre_completo = str(fila.get('apellido_paterno')) + ' ' + str(fila.get('apellido_materno')) + ' ' + str(fila.get('nombre_aspirante')),
                    numero_control = fila.get('no_control'),
                    carrera = fila.get('carrera')
                )
                alumno_nuevo.save()
        else:
            data['error'] = 'No subio ningun archivo, porfavor elija uno y subalo.'
    return render(request, 'importar.html', data)

def ControladorAltaAlumnos(request):
    data = {}
    if request.method == "POST":
        # Aqui entra cuando btn_registro
        data={
            'nombre_completo' : request.POST.get('txt_nombre'),
            'numero_control' : request.POST.get('txt_noControl'),
            'carrera' : request.POST.get('txt_carrera'),
        }
        try:
            insertarAlumno = Alumno(**data)
            insertarAlumno.save()
        except Exception as e:
            return render(request, '404.html')
    return render(request, 'alta_usuarios.html')

def ControladorSubirArchivos(request):
	'''El bloque try/except sirve para enviar texto placeholder en caso de
	no encontrar la vista.'''
	data = {}
	try:
		response = render(request, 'nombre_de_la_pantalla.html')
	except Exception as e:
		response = HttpResponse('El panadero con el pan XD (No hay html para esta parte aun).')
	return response

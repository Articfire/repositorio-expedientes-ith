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
    return HttpResponse("Inicio")

def ControladorImportarAlumnos(request):
    '''docstring para ControladorImportarAlumnos.'''
    data = {'error': None}
    if request.method == 'POST':
        if request.FILES.get('archivo'):
            mi_archivo = request.FILES.get('archivo')

            if '.xlsx' in mi_archivo.name:
                fs = FileSystemStorage()
                nombre_archivo = fs.save(mi_archivo.name, mi_archivo)

                info_excel = pd.read_excel(r'media/{}'.format(mi_archivo.name))
                diccionario_alumnos = info_excel.to_dict('index')

                for fila in diccionario_alumnos.values():
                    alumno_nuevo = Alumno(**fila)
                    alumno_nuevo.save()
            else:
                data['error'] = 'El archivo subido no es de excel, suba uno de excel (con la terminacion .xlsx).'
        else:
            data['error'] = 'No subio ningun archivo, porfavor elija uno y subalo.'
    return render(request, 'importar.html', data)

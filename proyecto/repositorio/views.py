from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import pandas as pd

from .models import Alumno, Archivo


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

def ControladorConsultaExpedientes(request):
    data = {}
    return render(request, 'consulta.html')

def ControladorExpediente(request, id):
    data = {'error' : None}
    try:
        alumno = Alumno.objects.get(id=id)
        data.update({'numero_control': alumno.numero_control})
    except Exception as e:
        data.update({'error' : 'No existe ese expediente en el repositorio.'})
        print(e)

    if request.method == 'POST' and not data.get('error'):
        if request.FILES.get('archivo'):
            # Obtener valores necesarios del POST y de la base de datos
            prefijo = request.POST.get('prefijo')

            # Proceso de renombrar archivo subido
            mi_archivo = request.FILES.get('archivo')
            ruta = mi_archivo.name.split('/')
            nombre_y_extension = ruta[-1].split('.')
            nombre_archivo = prefijo + '_' + str(data.get('numero_control')) + '.' + nombre_y_extension[-1]
            ruta[-1] = nombre_archivo
            mi_archivo.name = '/'.join(ruta)

            # Guardar archivo
            fs = FileSystemStorage()
            archivo_guardado = fs.save(mi_archivo.name, mi_archivo)

            archivo_anexado = Archivo(
                nombre = prefijo + '_' + str(data.get('numero_control')),
                ruta = 'media/',
                extension = nombre_y_extension[-1],
                pertenece_a = id
            )
        else:
            data.update({'error' : 'No subio ningun archivo, porfavor elija uno y subalo.'})
    return render(request, 'expediente.html', data)

def ControladorAjaxConsulta(request, busqueda, filtro):
    if request.method == 'POST':
        if filtro == 'nombre':
            alumnos = Alumno.objects.filter(nombre_completo = busqueda)
        elif filtro == 'numero_control':
            alumnos = Alumno.objects.filter(numero_control = busqueda)
        else:
            return HttpResponse('No hay un filtro '+str(filtro))
        data = list(alumnos)

    return HttpResponse('El metodo de peticion debe ser POST.')

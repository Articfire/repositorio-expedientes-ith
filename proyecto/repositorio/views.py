from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import pandas as pd
import json

from .models import Alumno, Archivo
from .overwrite_storage import OverwriteStorage

def ControladorInicio(request):
    data = {}
    return render(request, 'inicio.html')

def ControladorImportarAlumnos(request):
    '''docstring para ControladorImportarAlumnos.'''
    data = {'error': None}
    if request.method == 'POST':
        if request.FILES.get('archivo'):
            mi_archivo = request.FILES.get('archivo')
            fs = OverwriteStorage()
            nombre_archivo = fs.save(mi_archivo.name, mi_archivo)

            try:
                info_excel = pd.read_excel(r'media/{}'.format(mi_archivo.name))
                diccionario_alumnos = info_excel.to_dict('index')

            except Exception as e:
                data['error'] = 'El archivo que intentó subir no es de excel'
            finally:
                try:
                    for fila in diccionario_alumnos.values():
                        alumno_nuevo = Alumno(
                        nombre_completo = str(fila.get('apellido_paterno')) + ' ' + str(fila.get('apellido_materno')) + ' ' + str(fila.get('nombre_aspirante')),
                        numero_control = fila.get('no_control'),
                        carrera = fila.get('carrera')
                        )
                        alumno_nuevo.save()
                except Exception as e:
                    data['error'] = 'Error: Se trato de ingresar un numero de control repetido.'
        else:
            data['error'] = 'No se subio ningun archivo, porfavor elija uno y subalo.'
    return render(request, 'importar.html', data)

def ControladorAltaAlumnos(request):
    data = {'error' : None}
    if request.method == "POST":
        # validaciones del formulario
        if request.POST.get('txt_carrera') == "" and request.POST.get('carrera-personalizada') == "":
            data.update({'error' : 'Error: Debe elegir una opcion, elegir una carrera de la lista o escribir una carrera personalizada.'})
        elif not request.POST.get('txt_carrera') == "" and not request.POST.get('carrera-personalizada') == "":
            data.update({'error' : 'Error: No puede elegir una carrera y escribir una personalizada a la vez.'})
        elif not request.POST.get('txt_carrera') == "":
            carrera = request.POST.get('txt_carrera')
        else:
            carrera = request.POST.get('carrera-personalizada')

        try:
            alumno_a_registrar = Alumno(
                nombre_completo = request.POST.get('txt_nombre'),
                numero_control = request.POST.get('txt_noControl'),
                carrera = carrera,
            )
            if not 50 >= len(alumno_a_registrar.nombre_completo) >= 10 and not data['error']:
                data['error'] = "Error: El nombre completo debe tener entre 50 y 10 caracteres."
            elif not 8 >= len(alumno_a_registrar.numero_control) >= 7 and not data['error']:
                data['error'] = "Error: El numero de control debe tener entre 8 y 7 digitos."
            else:
                alumno_a_registrar.save()
        except Exception as ex:
            if not data['error']:
                data['error'] = str(ex)
    return render(request, 'alta_usuarios.html', data)

def ControladorConsultaExpedientes(request):
    return render(request, 'consulta.html')

def ControladorExpediente(request, id):
    data = {'error' : None}
    try:
        alumno = Alumno.objects.get(id=id)
    except Exception as e:
        return HttpResponse('No existe ese expediente de alumno en el repositorio.')

    archivos = Archivo.objects.filter(pertenece_a=Alumno(id))
    data.update({
        'nombre_completo': alumno.nombre_completo,
        'numero_control': alumno.numero_control,
        'archivos' : archivos,
    })

    if request.method == 'POST' and not data['error']:
        if request.POST.get('prefijo') == "" and request.POST.get('prefijo-personalizado') == "":
            data.update({'error' : 'Debe elegir una opcion.'})
        elif request.FILES.get('archivo'):
            # Obtener valores necesarios del POST y de la base de datos
            if request.POST.get('prefijo-personalizado') == "":
                prefijo = request.POST.get('prefijo')
            else:
                prefijo = request.POST.get('prefijo-personalizado')

            # Proceso para cambiarle el nombre al archivo subido a uno mas legible
            mi_archivo = request.FILES.get('archivo')
            ruta = mi_archivo.name.split('/')
            nombre_y_extension = ruta[-1].split('.')
            nombre_archivo = prefijo + '_' + str(data.get('numero_control')) + '.' + nombre_y_extension[-1]
            ruta[-1] = nombre_archivo
            mi_archivo.name = '/'.join(ruta)

            # Guardar o Sobreescribir el archivo.
            fs = OverwriteStorage()
            archivo_guardado = fs.save(mi_archivo.name, mi_archivo)

            # Preparar consulta para insertar a la tabla de archivos.
            nombre = prefijo + '_' + str(data.get('numero_control'))
            try:
                archivo_a_anexar = Archivo.objects.get(nombre=nombre)
                archivo_a_anexar.extension = nombre_y_extension[-1]
                archivo_a_anexar.pertenece_a = Alumno(id)
            except Archivo.DoesNotExist:
                archivo_a_anexar = Archivo(
                    nombre = nombre,
                    extension = nombre_y_extension[-1],
                    pertenece_a = Alumno(id)
                )
            archivo_a_anexar.save()
        else:
            data.update({'error' : 'Error: No subio ningun archivo, porfavor elija uno y subalo.'})
    return render(request, 'expediente.html', data)

def ControladorAjaxConsulta(request, busqueda, filtro):
    alumnos = None

    if filtro == 'nombre':
        alumnos = Alumno.objects.filter(nombre_completo__contains = busqueda)
    elif filtro == 'numero_control':
        alumnos = Alumno.objects.filter(numero_control__contains = busqueda)

    if alumnos:
        data = [
            {
                'id': alumno.id,
                'nombre_completo': alumno.nombre_completo,
                'numero_control': alumno.numero_control,
                'carrera': alumno.carrera,
            }
            for alumno in alumnos
        ]

        return HttpResponse(json.dumps(data, sort_keys=False, indent=4), content_type="application/json")
    else:
        return HttpResponse("Hubo un error, revisa que el filtro y la busqueda sean correctos.")

@login_required
def ControladorVerPDF(request, archivo_id):
    try:
        archivo = Archivo.objects.get(id=archivo_id)
        with open('{}/{}.{}'.format(settings.MEDIA_ROOT, archivo.nombre, archivo.extension), 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/{}'.format(archivo.extension))
            response['Content-Disposition'] = 'inline;filename={}.{}'.format(archivo.nombre, archivo.extension)
            return response
        pdf.closed
    except ValueError as ve:
        return ("No existe tal archivo.")

def ControladorLogin(request):
    if request.method=="POST":
        claveUsr = request.POST.get("txt_clave")
        passwrd = request.POST.get("txt_password")
        user = authenticate(username=claveUsr, password=passwrd)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    return render(request, 'login.html')

def ControladorLogout(request):
    logout(request)
    return redirect('/login')

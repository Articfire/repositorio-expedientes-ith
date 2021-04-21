from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def ControladorInicio(request):
    # render() es la manera mas facil de enviar html por una respuesta.
    # request es un objeto peticion con la informacion del navegador, etc.
    # template_name es un string con la ruta del template.
    return render(request, template_name = "ejemplo_de_vista.html")

def ControladorImportarAlumnos(request):
    if request.method == 'POST':
        try:
            # info_excel = pd.read_excel(r'ruta_al_archivo.xlsx')
            # info_excel.to_dict('index')
            pass
        except Exception as e:
            print(e)
    return HttpResponse("Importar Alumnos")

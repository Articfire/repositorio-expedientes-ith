from django.urls import path
from . import views

urlpatterns = [
    path('', views.ControladorInicio, name='inicio'),
    path('importar', views.ControladorImportarAlumnos, name='importar_alumnos'),
]

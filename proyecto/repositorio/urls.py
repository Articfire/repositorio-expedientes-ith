from django.urls import path
from . import views

urlpatterns = [
    path('', views.ControladorInicio, name='inicio'),
    path('importar', views.ControladorImportarAlumnos, name='importar_alumnos'),
    path('alta', views.ControladorAltaAlumnos, name='alta_alumnos'),
    path('expediente/<int:id>', views.ControladorExpediente, name='expediente'),
]

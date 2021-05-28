from django.urls import path
from . import views

urlpatterns = [
    path('', views.ControladorInicio, name='inicio'),
    path('importar', views.ControladorImportarAlumnos, name='importar_alumnos'),
    path('alta', views.ControladorAltaAlumnos, name='alta_alumnos'),
    path('consulta', views.ControladorConsultaExpedientes, 'consulta'),
    path('expediente/<int:id>', views.ControladorExpediente, name='expediente'),
    path('api/consulta', views.ControladorAjaxConsulta, name='api_consulta'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ControladorInicio, name='inicio'),
    path('importar', views.ControladorImportarAlumnos, name='importar_alumnos'),
    path('alta', views.ControladorAltaAlumnos, name='alta_alumnos'),
    path('consulta', views.ControladorConsultaExpedientes, name='consulta'),
    path('expediente/<int:id>', views.ControladorExpediente, name='expediente'),
    path('api/alumnos/<busqueda>/<filtro>', views.ControladorAjaxConsulta, name='api_consulta'),
    path('archivo/<int:archivo_id>', views.ControladorVerPDF, name='archivo')
]

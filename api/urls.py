# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('empresas/', EmpresaListCreateAPIView.as_view(), name='empresa-list-create'),
    path('tiposenvio/', TipoEnvioListCreate.as_view(), name='tiposenvio-list-create'),
    path('responsables/', views.responsable_list),
    path('responsables/<str:pk>/', views.responsable_detail),
    path('planillas/', PlanillaAPIView.as_view(), name='planilla-list'),
    path('planillas/<str:id>/', PlanillaAPIView.as_view(), name='planilla-detail'),
    path('emisor/', EmisorListCreateAPIView.as_view(), name='emisor-list-create'),
    path('turno/', TurnoListCreateAPIView.as_view(), name='turno-list-create'),
    path('consumidor/', ConsumidorListCreateAPIView.as_view(), name='consumidor-list-create'),
    path('importar-asistencia/', importar_asistencia_Post, name='importar_asistencia_list'),
    path('importar-asistencia-detalle/', views.importar_asistencia_list, name='importar_asistencia_list'),
    path('pota/importarasistencia/', POTAAsistenciaUpdateByCodigoGeneralView.as_view(), name='importar_asistencia_list'),
    path('pota/importarasistencia/<str:idcodigogeneral>/', POTAAsistenciaUpdateByCodigoGeneralView.as_view()),
    path('asistencia/<str:idcodigogeneral>/<str:idlabor>/', MerluzasistenciaUpdateByCodigoGeneralView.as_view(), name='update_asistencia'),

    path('estado/', estado_dia, name='estado_dia'),
    path('cerrar-dia/<str:fecha>/', cerrar_dia, name='cerrar_dia'),

    path('ingresos-dia-actual/', ingresos_del_dia_actual, name='ingresos-dia-actual'),
    path('ingresos-dia-actual/<str:idcodigogeneral>/', ingresos_del_dia_actual, name='ingresos_del_dia_actual_idcodigogeneral'),

    ]

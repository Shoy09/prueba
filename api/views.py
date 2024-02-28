from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Empresa
from .serializers import EmpresaSerializer

class EmpresaListCreateAPIView(APIView):
    def get(self, request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics
from .models import TipoEnvio
from .serializers import TipoEnvioSerializer

class TipoEnvioListCreate(generics.ListCreateAPIView):
    queryset = TipoEnvio.objects.all()
    serializer_class = TipoEnvioSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Responsable
from .serializers import ResponsableSerializer

@api_view(['GET', 'POST'])
def responsable_list(request):
    if request.method == 'GET':
        responsables = Responsable.objects.all()
        serializer = ResponsableSerializer(responsables, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def responsable_detail(request, pk):
    try:
        responsable = Responsable.objects.get(pk=pk)
    except Responsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResponsableSerializer(responsable)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ResponsableSerializer(responsable, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        responsable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Planilla
from .serializers import PlanillaSerializer

class PlanillaAPIView(APIView):
    def get(self, request):
        planillas = Planilla.objects.all()
        serializer = PlanillaSerializer(planillas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanillaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        planilla = Planilla.objects.get(idplanilla=id)
        serializer = PlanillaSerializer(planilla, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        planilla = Planilla.objects.get(idplanilla=id)
        planilla.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Emisor
from .serializers import EmisorSerializer

class EmisorListCreateAPIView(APIView):
    def get(self, request):
        emisor = Emisor.objects.all()
        serializer = EmisorSerializer(emisor, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmisorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Especie
from .serializers import EspecieSerializer

class EspecieListCreateAPIView(APIView):
    def get(self, request):
        especie = Especie.objects.all()
        serializer = EspecieSerializer(especie, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EspecieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Turno
from .serializers import TurnoSerializer

class TurnoListCreateAPIView(APIView):
    def get(self, request):
        turno = Turno.objects.all()
        serializer = TurnoSerializer(turno, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TurnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Consumidor
from .serializers import ConsumidorSerializer

class ConsumidorListCreateAPIView(APIView):
    def get(self, request):
        consumidor = Consumidor.objects.all()
        serializer = ConsumidorSerializer(consumidor, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsumidorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from .models import ImportarAsistencia, EstadoDia, ImportarAsistenciaDetalle
from .serializers import ImportarAsistenciaSerializer, ImportarAsistenciaDetalleSerializer

from datetime import datetime

@api_view(['POST'])
@transaction.atomic
def importar_asistencia_Post(request):
    if request.method == 'POST':
        try:
            # Obtener la fecha actual en tiempo real en formato YYYYMMDD
            fecha_actual = datetime.now().strftime('%Y%m%d')

            # Verificar si el día está abierto
            estado = EstadoDia.determinar_estado(fecha_actual)
            if not estado:
                return Response({"error": "El día está cerrado. No se pueden importar asistencias en este momento."},
                                status=status.HTTP_403_FORBIDDEN)

            idcodigogeneral = request.data.get('idcodigogeneral')

            # Verificar si ya existe un registro para idcodigogeneral en la fecha actual
            existing_importaciones = ImportarAsistenciaDetalle.objects.filter(
                idcodigogeneral=idcodigogeneral,
                importar_asistencia__fecha=fecha_actual
            )
            if existing_importaciones.exists():
                return Response({"error": "Ya se ha importado la asistencia para este idcodigogeneral hoy."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Crear la instancia de ImportarAsistencia
            importar_asistencia_data = {
                'idempresa': request.data.get('idempresa'),
                'tipo_envio': request.data.get('tipo_envio'),
                'idresponsable': request.data.get('idresponsable'),
                'idplanilla': request.data.get('idplanilla'),
                'idemisor': request.data.get('idemisor'),
                'idturno': request.data.get('idturno'),
                'fecha': fecha_actual,
                'idsucursal': request.data.get('idsucursal'),
                'idespecie': request.data.get('idespecie')  # Asegúrate de agregar el campo idespecie
            }
            importar_asistencia_serializer = ImportarAsistenciaSerializer(data=importar_asistencia_data)
            importar_asistencia_serializer.is_valid(raise_exception=True)
            importar_asistencia = importar_asistencia_serializer.save()

            # Crear las instancias de ImportarAsistenciaDetalle
            detalle_data = request.data.get('detalle', [])
            for detalle_item in detalle_data:
                detalle_item['importar_asistencia'] = importar_asistencia.pk
                detalle_serializer = ImportarAsistenciaDetalleSerializer(data=detalle_item)
                detalle_serializer.is_valid(raise_exception=True)
                detalle_serializer.save()

            return Response(importar_asistencia_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImportarAsistenciaDetalle
from .serializers import AsistenciaSerializer, AsistenciaDetalleSerializer

class MerluzasistenciaUpdateByCodigoGeneralView(APIView):
    def put(self, request, idcodigogeneral, idlabor):
        try:
            # Obtener la fecha actual
            fecha_actual = datetime.now().strftime("%Y%m%d")
            
            # Buscar el registro de ImportarAsistenciaDetalle por idcodigogeneral e idlabor y fecha actualizada
            asistencia_detalle = ImportarAsistenciaDetalle.objects.get(idcodigogeneral=idcodigogeneral, idlabor=idlabor, importar_asistencia__fecha__gte=fecha_actual)
            
            # Actualizar la cantidad si existe en los datos de la solicitud
            if 'cantidad' in request.data:
                asistencia_detalle.cantidad = request.data['cantidad']
                asistencia_detalle.save()
                
                # Obtener la asistencia actualizada
                asistencia = asistencia_detalle.importar_asistencia
                
                # Serializar la asistencia y sus detalles
                serializer = AsistenciaSerializer(asistencia)
                data = serializer.data
                detalles = AsistenciaDetalleSerializer(asistencia.detalle.all(), many=True).data
                data['detalle'] = detalles
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "La cantidad no se proporcionó en los datos de la solicitud"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ImportarAsistenciaDetalle.DoesNotExist:
            return Response({"error": "No se encontró el registro de ImportarAsistenciaDetalle con idcodigogeneral e idlabor proporcionados o la fecha de actualización es anterior a la fecha actual"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def importar_asistencia_list(request):
    try:
        importar_asistencias = ImportarAsistencia.objects.all()
        data = []
        for importar_asistencia in importar_asistencias:
            serializer = ImportarAsistenciaSerializer(importar_asistencia)
            detalle_serializer = ImportarAsistenciaDetalleSerializer(importar_asistencia.detalle.all(), many=True)
            importar_asistencia_data = serializer.data
            importar_asistencia_data['detalle'] = detalle_serializer.data
            data.append(importar_asistencia_data)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# ------------------------------------------------------------------------------------

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImportarAsistencia
from .serializers import AsistenciaSerializer, AsistenciaDetalleSerializer

class POTAAsistenciaUpdateByCodigoGeneralView(APIView):
    def get(self, request, codigo_general=None):
        # Verificar si el día está abierto
        estado = EstadoDia.determinar_estado(timezone.now().date())
        if not estado:
            return Response({"error": "El día está cerrado. No se pueden realizar operaciones en las asistencias."},
                            status=status.HTTP_403_FORBIDDEN)

        if codigo_general is not None:
            try:
                asistencia = ImportarAsistencia.objects.get(idcodigogeneral=codigo_general)
                # Serializar la asistencia y sus detalles
                serializer = ImportarAsistenciaSerializer(asistencia)
                data = serializer.data
                detalles = ImportarAsistenciaDetalleSerializer(asistencia.detalle.all(), many=True).data
                data['detalle'] = detalles
                return Response(data, status=status.HTTP_200_OK)
            except ImportarAsistencia.DoesNotExist:
                return Response({'error': 'Asistencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        else:
            importar_asistencias = ImportarAsistencia.objects.all()
            data = []
            for importar_asistencia in importar_asistencias:
                asistencia_data = ImportarAsistenciaSerializer(importar_asistencia).data
                detalles = ImportarAsistenciaDetalleSerializer(importar_asistencia.detalle.all(), many=True).data
                asistencia_data['detalle'] = detalles
                data.append(asistencia_data)
            return Response(data, status=status.HTTP_200_OK)

    def put(self, request, idcodigogeneral):
        try:
            # Buscar el registro de ImportarAsistenciaDetalle por idcodigogeneral
            asistencia_detalle = ImportarAsistenciaDetalle.objects.get(idcodigogeneral=idcodigogeneral)
            
            # Actualizar la cantidad si existe en los datos de la solicitud
            if 'cantidad' in request.data:
                asistencia_detalle.cantidad = request.data['cantidad']
                asistencia_detalle.save()
                
                # Obtener la asistencia actualizada
                asistencia = asistencia_detalle.importar_asistencia
                
                # Serializar la asistencia y sus detalles
                serializer = AsistenciaSerializer(asistencia)
                data = serializer.data
                detalles = AsistenciaDetalleSerializer(asistencia.detalle.all(), many=True).data
                data['detalle'] = detalles
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "La cantidad no se proporcionó en los datos de la solicitud"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ImportarAsistenciaDetalle.DoesNotExist:
            return Response({"error": "No se encontró el registro de ImportarAsistenciaDetalle con idcodigogeneral proporcionado"}, status=status.HTTP_404_NOT_FOUND)
#---------------------------------------------------
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EstadoDia
from .serializers import EstadoDiaSerializer
from django.utils import timezone
from datetime import datetime


@api_view(['POST'])
def estado_dia(request):
    if request.method == 'POST':
        # Obtener la fecha actual en formato YYYY-MM-DD
        fecha_actual = datetime.now().date()

        # Verificar si ya existe un registro para la fecha actual
        if EstadoDia.objects.filter(fecha=fecha_actual).exists():
            return Response({"error": "El día ya está abierto."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Crear un nuevo registro para la fecha actual
        estado = EstadoDia.objects.create(fecha=fecha_actual, abierto=True)
        return Response({"message": "El día se ha abierto correctamente."},
                        status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def cerrar_dia(request, fecha):
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()  # Convertir la fecha a un objeto datetime.date
        estado = EstadoDia.objects.get(fecha=fecha)
    except EstadoDia.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Verificar si el día ya está cerrado
    if estado.hora_cierre is not None:
        return Response({"message": "El día ya está cerrado"}, status=status.HTTP_400_BAD_REQUEST)

    estado.cerrar_dia()
    serializer = EstadoDiaSerializer(estado)
    return Response(serializer.data)

from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ImportarAsistencia
from .serializers import ImportarAsistenciaSerializer

@api_view(['GET'])
def ingresos_del_dia_actual(request, idcodigogeneral=None):
    try:
        # Obtener la fecha actual en formato YYYYMMdd
        fecha_actual = timezone.now().strftime('%Y%m%d')
        
        # Filtrar los registros de ImportarAsistencia por la fecha actual y el idcodigogeneral si se proporciona
        importar_asistencias = ImportarAsistencia.objects.filter(fecha=fecha_actual)
        
        if idcodigogeneral:
            importar_asistencias = importar_asistencias.filter(detalle__idcodigogeneral=idcodigogeneral)
        
        # Usamos distinct para asegurarnos de obtener resultados únicos
        importar_asistencias = importar_asistencias.distinct()

        # Serializar los datos y sus detalles
        data = []
        for importar_asistencia in importar_asistencias:
            asistencia_data = ImportarAsistenciaSerializer(importar_asistencia).data
            detalles = []
            for detalle in importar_asistencia.detalle.all():
                detalle_data = {
                    "item": detalle.item,
                    "idcodigogeneral": detalle.idcodigogeneral,
                    "idactividad": detalle.idactividad,
                    "idlabor": detalle.idlabor,
                    "idconsumidor": detalle.idconsumidor,
                    "cantidad": detalle.cantidad
                }
                detalles.append(detalle_data)
            asistencia_data['detalle'] = detalles
            data.append(asistencia_data)
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

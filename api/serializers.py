from rest_framework import serializers
from .models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('idempresa', 'nombre')
        read_only_fields = ('idempresa',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Empresa.objects.create(**validated_data)


from rest_framework import serializers
from .models import TipoEnvio

class TipoEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEnvio
        fields = '__all__'


from .models import Responsable
class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ('idresponsable', 'nombre_apellido')
        read_only_fields = ('idresponsable',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Responsable.objects.create(**validated_data)

from rest_framework import serializers
from .models import Planilla

class PlanillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planilla
        fields = ['idplanilla', 'nombre']

from rest_framework import serializers
from .models import Emisor

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor
        fields = ('idemisor', 'nombre')
        read_only_fields = ('idemisor',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Emisor.objects.create(**validated_data)
    

    from rest_framework import serializers
from .models import Especie

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ('idespecie', 'nombre')
        read_only_fields = ('idespecie',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Especie.objects.create(**validated_data)

from .models import Turno

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ('idturno', 'nombre')
        read_only_fields = ('idturno',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Turno.objects.create(**validated_data)



    

from .models import Consumidor
class ConsumidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumidor
        fields = ('idconsumidor', 'nombre_apellido')
        read_only_fields = ('idconsumidor',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Consumidor.objects.create(**validated_data)


# ------------------------------------------------------------------------------------

from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework import status
from .models import ImportarAsistencia
from datetime import datetime

class ImportarAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistencia
        fields = '__all__'

    def create(self, validated_data):
        # Obtener la fecha actual en formato YYYYMMdd
        fecha_actual = datetime.now().strftime('%Y%m%d')
        # Asignar la fecha actual al campo 'fecha' en los datos validados
        validated_data['fecha'] = fecha_actual
        
        # Crear y devolver la instancia del modelo ImportarAsistencia
        return ImportarAsistencia.objects.create(**validated_data)
    
class ImportarAsistenciaList(generics.ListCreateAPIView):
    queryset = ImportarAsistencia.objects.all()
    serializer_class = ImportarAsistenciaSerializer

class ImportarAsistenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImportarAsistencia.objects.all()
    serializer_class = ImportarAsistenciaSerializer


# ImportarAsistenciaDetalleSerializer
from rest_framework import serializers
from .models import ImportarAsistenciaDetalle

class ImportarAsistenciaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistenciaDetalle
        fields = '__all__'

    def create(self, validated_data):
        # Crear y devolver la instancia del modelo ImportarAsistenciaDetalle
        return ImportarAsistenciaDetalle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar y devolver la instancia del modelo ImportarAsistenciaDetalle
        instance.idcodigogeneral = validated_data.get('idcodigogeneral', instance.idcodigogeneral)
        instance.idactividad = validated_data.get('idactividad', instance.idactividad)
        instance.idlabor = validated_data.get('idlabor', instance.idlabor)
        instance.idconsumidor = validated_data.get('idconsumidor', instance.idconsumidor)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.save()
        return instance


# ------------------------------------------------------------------------------------
from rest_framework import serializers
from .models import ImportarAsistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistencia
        fields = '__all__'

#---------------------------------------------------
from rest_framework import serializers
from .models import EstadoDia

class EstadoDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoDia
        fields = '__all__'



from rest_framework import serializers
from .models import ImportarAsistencia, ImportarAsistenciaDetalle

class ImportarAsistenciaSerializer(serializers.ModelSerializer):
    detalle = serializers.SerializerMethodField()

    class Meta:
        model = ImportarAsistencia
        fields = ['id', 'idempresa', 'tipo_envio', 'idresponsable', 'idplanilla', 'idemisor', 'idturno', 'fecha', 'idsucursal', 'idespecie', 'detalle']

    def get_detalle(self, obj):
        detalle_queryset = obj.detalle.all()
        return AsistenciaDetalleSerializer(detalle_queryset, many=True).data

class AsistenciaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistenciaDetalle
        fields = ['item', 'idcodigogeneral', 'idactividad', 'idlabor', 'idconsumidor', 'cantidad', 'importar_asistencia']

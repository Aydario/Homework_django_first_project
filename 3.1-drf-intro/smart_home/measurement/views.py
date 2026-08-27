from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from .models import Sensor, Measurement
from .serializers import (
    SensorSerializer, 
    SensorDetailSerializer, 
    MeasurementCreateSerializer
)

class SensorListCreateView(ListCreateAPIView):
    """
    GET: Получить список датчиков
    POST: Создать новый датчик
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorRetrieveUpdateView(RetrieveUpdateAPIView):
    """
    GET: Получить информацию по конкретному датчику
    PATCH/PUT: Обновить датчик
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class MeasurementCreateView(CreateAPIView):
    """
    POST: Добавить измерение для датчика
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer
    
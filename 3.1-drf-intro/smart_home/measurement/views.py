import inspect

from rest_framework import generics, viewsets

from datetime import datetime
from django.http import HttpResponse

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer
from measurement.serializers import SensorDetailSerializer
from measurement.serializers import MeasurementPostSerializer


def time_view(request):
    current_time = datetime.now()
    msg = '{current_time: %s}' % current_time
    return HttpResponse(msg, content_type='application/json')


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        caller_frame = inspect.currentframe().f_back.f_back
        code_obj_name = caller_frame.f_code.co_name

        if code_obj_name == 'retrieve':
            return SensorDetailSerializer
        else:
            return SensorSerializer


class MeasurementCreateAPIView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementPostSerializer

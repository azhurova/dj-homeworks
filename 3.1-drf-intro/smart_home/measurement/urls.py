from django.urls import path
from measurement.views import SensorViewSet, MeasurementCreateAPIView
from measurement.views import time_view

urlpatterns = [
    path('sensors/', SensorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sensors/<pk>', SensorViewSet.as_view({'get': 'retrieve',
                                                'patch': 'partial_update'})),
    path('measurements/', MeasurementCreateAPIView.as_view()),
    path('current_time/', time_view, name='time'),
]

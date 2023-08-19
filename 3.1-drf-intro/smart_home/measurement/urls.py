from django.urls import path
from measurement.views import SensorViewSet, MeasurementCreateAPIView

urlpatterns = [
    path('sensors/', SensorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sensors/<pk>', SensorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('measurements/', MeasurementCreateAPIView.as_view()),
]

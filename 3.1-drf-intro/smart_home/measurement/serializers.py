from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from measurement.models import Measurement, Sensor


class MeasurementPostSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=False, required=False)

    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)

    def get_validation_exclusions(self):
        exclusions = super(MeasurementPostSerializer, self)\
            .get_validation_exclusions()
        return exclusions + ['image']


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

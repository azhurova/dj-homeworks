from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)  # measurements


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                               related_name='measurements')
    temperature = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)

    class Meta:
        ordering = ['-created_at']

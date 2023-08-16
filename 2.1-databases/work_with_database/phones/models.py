from django.db import models
from pytils.translit import slugify


class Phone(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=512, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=512)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

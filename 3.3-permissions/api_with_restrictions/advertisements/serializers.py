from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'creator', 'created_at',
                  'status', 'title', 'description']
        read_only_fields = ['id', 'creator', 'created_at']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context["request"].user

        open_advertisements = Advertisement.objects.all().filter(creator=user, status=AdvertisementStatusChoices.OPEN)
        if self.instance:
            open_advertisements = open_advertisements.exclude(id=self.instance.id)
            advertisement_status = self.instance.status
        else:
            advertisement_status = AdvertisementStatusChoices.OPEN
        if 'status' in data:
            advertisement_status = data['status']

        if advertisement_status == AdvertisementStatusChoices.OPEN and open_advertisements.count() >= 10:
            raise ValidationError("У пользователя может быть не больше 10 открытых объявлений")

        return data

from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrSuperuser
from advertisements.serializers import AdvertisementSerializer


class AdvertisementFilter(rest_framework.FilterSet):
    created_at = rest_framework.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['title', 'status', 'creator', 'created_at', 'updated_at']

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filterset_fields = ['title', 'status', 'creator', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'status', 'creator']
    ordering_fields = ['id', 'title', 'status', 'creator', 'created_at', 'updated_at']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrSuperuser()]
        return []

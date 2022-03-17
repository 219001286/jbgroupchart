from rest_framework.serializers import ModelSerializer
from base.models import Department


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
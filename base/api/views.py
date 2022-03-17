from urllib import response
from base.views import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Department
from .serializers import RoomSerializer


@api_view(['GET'])
def getroutes(request):
    Routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/roooms/:id'

    ]
    return Response(Routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Department.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    room = Department.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


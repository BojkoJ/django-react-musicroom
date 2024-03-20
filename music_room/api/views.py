from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class RoomView(generics.ListAPIView):
    # Toto view bude sloužit k vytvoření nové místnosti
    queryset = Room.objects.all() # Vrací všechny místnosti
    serializer_class = RoomSerializer # Použije RoomSerializer

class CreateRoomView(APIView):
    # Co nám APIView dovoluje, je to, že můžeme přepsat metody jako get, post, put, delete, atd.
    # Toto view bude sloužit k vytvoření nové místnosti

    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # Pokud session neexistuje, vytvoříme novou
            self.request.session.create()

        # Vytvoříme nový serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            
            # Pokud místnost již existuje, tak ji updatneme
            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
            
            return Response(RoomSerializer(room).data,status=status.HTTP_201_CREATED)
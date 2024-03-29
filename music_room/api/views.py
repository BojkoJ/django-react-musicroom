from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all() # Vrací všechny místnosti
    serializer_class = RoomSerializer # Použije RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    # Použijeme metodu get, kde získáme kód místnosti
    def get(self, request, format=None):

        # Získáme kód místnosti pomocí request.GET.get metody, která bere lookup_url_kwarg jako argument
        # lookup_url_kwarg je proměnná, která obsahuje název URL parametru, který chceme získat
        code = request.GET.get(self.lookup_url_kwarg) 

        if code != None:
            # Vyfiltrujeme místnost podle kódu
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                # Serialuzujeme místnost a vrátíme ji
                data = RoomSerializer(room[0]).data
                
                # Do data přidáme is_host, který bude True, pokud je hostem
                # To pokud je hostem zjistím tak, že porovnám session_key s hostem místnosti (objekt room[0])
                data['is_host'] = self.request.session.session_key == room[0].host

                return Response(data, status=status.HTTP_200_OK)
            
            return Response({'Room not found' : 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request' : 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # Pokud session neexistuje, vytvoříme novou
            self.request.session.create()
        
        # získáme code z requestu
        code = request.data.get(self.lookup_url_kwarg)

        if code != None:
            room_result = Room.objects.filter(code=code)

            if len(room_result) > 0:
                room = room_result[0]

                # Toto nám řekne: "tento uživatel v jeho aktuální session je v této místnosti"

                # Co děláme je, že vytváříme dočasný storage object
                # který se jmenuje room_code a rovná se proměnné code
                # a uloží se do session usera
                self.request.session['room_code'] = code
                return Response({'message' : 'Room Joined!'}, status=status.HTTP_200_OK)
            
            return Response({'Bad Request' : 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'Bad Request' : 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


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
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request' : 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserInRoom(APIView):
    # na tento endpoint pošleme get request
    # endpoint bude checkovat: Je tento user v místnosti? 
    # Jestli ano, tento endpoint vrátí kód místnosti

    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # Pokud session neexistuje, vytvoříme novou
            self.request.session.create()
        
        data = {
            'code': self.request.session.get('room_code')
        }

        # JsonResponse dělá to, že vezme python dictionary a převede ho na JSON
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):

        if 'room_code' in self.request.session:
            # Pokud session obsahuje room_code, tak ho odstraníme 
            self.request.session.pop('room_code')

            # Pokud je rovněž user majitelem místnosti, smažeme ji:

            # Získáme session_key
            host_id = self.request.session.session_key

            # Získáme místnost kterou má host
            room_results = Room.objects.filter(host=host_id)

            # Pokud místnost existuje, tak ji smažeme
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({'Message' : 'Success'}, status=status.HTTP_200_OK)
    
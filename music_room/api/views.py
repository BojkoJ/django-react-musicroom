from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room

# Create your views here.

class RoomView(generics.CreateAPIView):
    # Toto view bude sloužit k vytvoření nové místnosti
    queryset = Room.objects.all() # Vrací všechny místnosti
    serializer_class = RoomSerializer # Použije RoomSerializer
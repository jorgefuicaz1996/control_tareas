from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
'''
class EntidadView(APIView):
	def get(self, request):
		data = Mensaje.objects.all()
		serializer = MensajeSerializer(data, many = True)
		return Response(serializer.data)
'''

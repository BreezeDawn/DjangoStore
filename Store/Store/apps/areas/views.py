from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from areas.models import Area
from areas.serializers import AreaSerializer


class AreasTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'areas'}, status=status.HTTP_200_OK)


class ProvincesView(ListAPIView):
    """省级接口"""
    queryset = Area.objects.filter(parent=None)
    serializer_class = AreaSerializer



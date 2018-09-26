
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from areas.models import Area
from areas.serializers import AreaSerializer,SubAreaSerializer


class AreasTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'areas'}, status=status.HTTP_200_OK)


class AreaViewSet(ReadOnlyModelViewSet):
    """集成List/Retrieve/GenericView为一体的视图集"""

    def get_serializer_class(self):
        """根据操作指定序列化器"""
        if self.action == 'retrieve':
            return SubAreaSerializer
        else:
            return AreaSerializer

    def get_queryset(self):
        """根据操作指定查询集"""
        if self.action == 'retrieve':
            return Area.objects.all()
        else:
            return Area.objects.filter(parent=None)


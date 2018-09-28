
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializer,SubAreaSerializer


class AreasTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'areas'}, status=status.HTTP_200_OK)


class AreaViewSet(ReadOnlyModelViewSet,CacheResponseMixin):
    """
    1.集成List/Retrieve/GenericView为一体的视图集
    2.使用缓存,当某个用户访问某个地区后,将返回结果放在服务器缓存中,其他用户访问同一个url地址时,直接从缓存中获取结果并返回.
    3.ListCacheResponseMixin结合ListModelMixin一起用,
      RetrieveCacheResponseMixin结合RetrieveModelMixin一起用,
      CacheResponseMixin结合ListModelMixin和RetrieveModelMixin一起用
    """

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


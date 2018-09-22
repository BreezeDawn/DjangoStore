# Create your views here.
from urllib import parse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from QQ.utils import OAuthQQ


class QQTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'QQ'}, status=status.HTTP_200_OK)

class QQLoginView(APIView):
    def get(self,request):
        # 获取地址中的next参数
        next = request.query_params.get('next','/')
        # 组织登录QQ的url和参数
        QQ = OAuthQQ(state=next)
        url = QQ.get_login_url()
        return Response({'login_url':url})


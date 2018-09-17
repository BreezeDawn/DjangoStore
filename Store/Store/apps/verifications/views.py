# Create your views here.
import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class VerificationsTest(APIView):
    """测试接口"""
    def get(self, request):
        return Response({"api": 'verificationstest'}, status=status.HTTP_200_OK)


class SMSCodeView(APIView):
    """获取短信验证码"""
    def get(self, request, mobile):
        return Response({"mobile": mobile}, status=status.HTTP_200_OK)

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UsersTest(APIView):
    """测试接口"""
    def get(self, request):
        return Response({"api": 'users'}, status=status.HTTP_200_OK)
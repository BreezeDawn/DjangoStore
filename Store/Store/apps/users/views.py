# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class UsersTest(APIView):
    """测试接口"""
    def get(self, request):
        return Response({"api": 'users'}, status=status.HTTP_200_OK)

class UsersCount(APIView):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        data = {
            'username':username,
            'count':count
        }
        return Response(data)


class MobilesCount(APIView):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile':mobile,
            'count':count
        }
        return Response(data)
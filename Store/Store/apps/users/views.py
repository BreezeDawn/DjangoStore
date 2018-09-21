# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import Serializer


from users.models import User
from users.serializers import CreateUserSerializer


class UsersTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'users'}, status=status.HTTP_200_OK)


class UsersCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobilesCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UsersRegisterView(CreateAPIView):
    # 指明所用序列化器
    serializer_class = CreateUserSerializer

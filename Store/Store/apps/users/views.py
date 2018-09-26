# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer


class UsersTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'users'}, status=status.HTTP_200_OK)


class EmailVerifyView(APIView):
    def put(self,request):
        # 获取token
        token = request.query_params.get('token')
        if token is None:
            return Response({'message':'缺少token参数'},status=status.HTTP_400_BAD_REQUEST)
        user = User.check_verify_email(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})


class EmailView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    """使用RetrieveAPIView获取当前用户详细信息"""
    # 指定当前视图所用的权限控制类
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    # 改写get_object方法返回当前用户
    def get_object(self):
        return self.request.user


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

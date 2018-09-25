# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer


class UsersTestView(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'users'}, status=status.HTTP_200_OK)


class EmailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user

    def put(self,request):
        # 获取用户
        user = self.get_object()

        # 获取email并进行校验邮箱格式
        serializer = self.get_serializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置email
        serializer.save()

        # 返回应答
        return Response(serializer.data)


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

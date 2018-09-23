# Create your views here.
from urllib import parse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from QQ.exceptions import QQAPIError
from QQ.models import AuthModel
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

class QQCallBackView(APIView):
    def get(self,request):
        # 1.获取code并进行校验
        code = request.query_params.get('code')
        if code is None:
            return Response({'message':'缺少code参数'},status=status.HTTP_400_BAD_REQUEST)
        # 2.获取QQ登录用户的openid
        QQ = OAuthQQ()
        try:
            # 根据coed请求QQ服务器获取access_token
            token = QQ.get_access_token(code)
            # 根据access_token请求QQ服务器获取openid
            openid = QQ.get_openid(token)
        except QQAPIError:
            return Response({'message':'QQ登录异常'},status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 3.根据openid进行处理
        try:
            qq_user = AuthModel.objects.get(openid=openid)
        except AuthModel.DoesNotExist:
            # 用户第一次使用QQ登录,绑定用户界面
            openid_token = QQ.generate_save_user_token(openid)
            return Response({'openid_token':openid_token})
        else:
            # 之前使用过QQ登录,签发jwt token 并返回
            user = qq_user.user  # 使用外键得到用户

            # 由服务器生成一个jwt-token数据,包含登录用户身份信息(以下五行->drf-jwt官方文档)
            from rest_framework_jwt.settings import api_settings

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 生成载荷
            payload = jwt_payload_handler(user)
            # 生成jwt-token
            token = jwt_encode_handler(payload)

            # 返回响应
            resp_data = {
                'user_id':user.id,
                'username':user.usernamem,
                'token':token
            }
            return Response(resp_data)


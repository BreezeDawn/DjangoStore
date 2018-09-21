def jwt_response_payload_handler(token, user=None, request=None):
    """自定义JWT自有登录视图返回值"""
    return {
        'user_id':user.id,
        'username':user.username,
        'token': token,
    }
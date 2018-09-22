
# Create your tests here.

# if __name__ == '__main__':
    # from itsdangerous import TimedJSONWebSignatureSerializer
    # secret_key 密匙 expires_in 有效期内解密
    # TJWSS = TimedJSONWebSignatureSerializer(secret_key='123123',expires_in=3600)
    # Json = {
    #     'openid':'123123123123'
    # }
    # 加密并返回加密后的数据
    # print(TJWSS.dumps(Json))
    # 解密并返回解密后的数据
    # print(TJWSS.loads(TJWSS.dumps(Json)))



# if __name__ == "__main__":
#     # urlopen: 发送网络请求
#     from urllib.request import urlopen
#
#     # 请求地址
#     req_url = 'http://api.meiduo.site:8000/mobiles/13155667788/count/'
#
#     # 发送网络请求
#     response = urlopen(req_url)
#
#     # 获取响应数据
#     res_data = response.read() # bytes 注: 响应数据为bytes类型
#     print(res_data)

# if __name__ == "__main__":
#     # parse_qs: 将查询字符串转换为python字典
#     from urllib.parse import parse_qs
#
#     # 定义查询字符串
#     req_data = 'c=3&b=2&a=1&c=4'
#
#     res = parse_qs(req_data) # 注: key对应的value是list
#     print(res)


# if __name__ == "__main__":
#     # urlencode: 将python字典转换为查询字符串
#     from urllib.parse import urlencode
#
#     # 定义字典
#     req_dict = {
#         'a': 1,
#         'b': 2,
#         'c': 3
#     }
#
#     res = urlencode(req_dict)
#     print(res)

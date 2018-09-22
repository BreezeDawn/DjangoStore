
# Create your tests here.

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

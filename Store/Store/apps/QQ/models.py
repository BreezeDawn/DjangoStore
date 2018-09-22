from django.db import models

# Create your models here.
from Store.utils.models import BaseModel


class AuthModel(BaseModel):
    # 外键不在同一子应用下,需要指明子应用,所以不能直接写User
    user = models.ForeignKey('users.User',on_delete=models.CASCADE,verbose_name="用户")
    # db_index 为该字段建立索引,提高查询速度
    openid = models.CharField(max_length=64,verbose_name="OpenID",db_index=True)

    class Meta:
        db_table = 'st_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name
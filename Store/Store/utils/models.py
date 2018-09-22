from django.db import models


class BaseModel(models.Model):
    """抽象模型基类"""
    # auto_now_add 该字段自动设置为创建时的时间
    create_time = models.DateField(auto_now_add=True,verbose_name="创建时间")
    # auto_now 修改数据时该字段自动更改修改数据时的时间
    update_time = models.DateField(auto_now=True,verbose_name="修改时间")

    class Meta:
        # 指定此模型是一个抽象模型,在进行迁移时不生成表
        abstract = True

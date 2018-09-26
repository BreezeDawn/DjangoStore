from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        # 绑定的模型
        model = Area
        # 需要序列化/反序列化哪些字段
        fields = ('id','name')

class SubAreaSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')

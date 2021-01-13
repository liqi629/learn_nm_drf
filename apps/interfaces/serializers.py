
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.interfaces.models import Interfaces
from apps.projects.models import Projects
from utils import validates


class InterfacesModelSerializer(serializers.ModelSerializer):
    """
    接口序列化器
    """

    name = serializers.CharField(label='接口名称',max_length=200,min_length=6,help_text='接口名称',validators=
                                 [UniqueValidator(queryset=Interfaces.objects.all(),message='接口名称不可重复')],
                                 error_messages={'max_length':'长度不超过200字节','min_length':'长度不少于6字节'})
    project = serializers.StringRelatedField(help_text="项目名称")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),help_text="项目ID")
    class Meta:
        model = Interfaces
        fields =  ('id', 'name', 'tester', 'project','project_id', 'desc', 'create_time')
        extra_kwargs = {
            'create_time':{
                'read_only':True
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        interface = Interfaces.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        if "project_id" in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance,validated_data)


class InterfacesRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Interfaces
        fields = ('id','env_id')


from rest_framework import serializers

from apps.projects.models import Projects
from apps.interfaces.models import Interfaces
from apps.debugtalks.models import DeubgTalks

from utils import validates



class ProjectModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Projects

        exclude = ('update_time','is_delete')
        extra_kwargs = {
            'create_time':{
                'read_only':True,
            }
        }

    def create(self, validated_data):
        project_obj = super().create(validated_data)
        DeubgTalks.objects.create(project=project_obj)
        return project_obj

class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id','name')

class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name','tester')

class InterfacesByProjectIdSerializer(serializers.ModelSerializer):

    interfaces = InterfaceNameSerializer(read_only=True,many=True)
    class Meta:
        model = Projects
        fields = ('id','interfaces')

class ProjectsRunSerializer(serializers.ModelSerializer):
    """
    通过项目运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Projects
        fields = ('id','env_id')
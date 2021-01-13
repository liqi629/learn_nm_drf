
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.testsuites.models import Testsuites
from utils import validates
from utils.validates import whether_existed_project_id

class TestsuitesSerializer(serializers.ModelSerializer):
    """
    测试套件序列化器
    """
    # 项目id
    project = serializers.StringRelatedField(help_text='项目ID')

    # 项目id
    project_id = serializers.IntegerField(write_only=True, validators=[whether_existed_project_id], help_text='项目ID')
    class Meta:
        model = Testsuites
        fields = '__all__'
        extra_kwargs = {
            'create_time':{
                'read_only':True
            }
        }


class TestsuitesRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testsuites
        fields = ('id','env_id')



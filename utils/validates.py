
from rest_framework import serializers

from apps.projects.models import Projects
from apps.interfaces.models import Interfaces
from apps.envs.models import Envs




def whether_existed_project_id(value):
    """
    检查项目
    :return:
    """
    if not isinstance(value,int):
        raise serializers.ValidationError('所选项目有误！')
    elif not Projects.objects.filter(is_delete=False,id=value).exists():
        raise serializers.ValidationError('所选项目不存在')

def whether_existed_interface_id(value):
    """
    检查接口
    :return:
    """
    if not isinstance(value,int):
        raise serializers.ValidationError('所选接口有误！')
    elif not Interfaces.objects.filter(is_delete=False,id=value).exists():
        raise serializers.ValidationError('所选接口不存在')


def whether_existed_env_id(value):
    """
    检查环境配置
    :return:
    """
    if value !=0:
        if not Envs.objects.filter(is_delete=False,id=value).exists():
            raise serializers.ValidationError('所选环境不存在')

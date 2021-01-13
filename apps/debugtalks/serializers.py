
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.debugtalks.models import DeubgTalks
from apps.projects.models import Projects

class DeubgTalksSerializer(serializers.ModelSerializer):
    """
    debugtalks序列化器
    """
    project = serializers.StringRelatedField(help_text='项目名称')


    class Meta:
        model = DeubgTalks
        # fields =  ('id', 'name', 'base_url', 'desc', 'create_time')
        exclude = ('is_delete', 'create_time', 'update_time')
        read_only_fields = ('name', 'project')
        extra_kwargs = {
            'debugtalk':{
                'write_only':True
            }
        }



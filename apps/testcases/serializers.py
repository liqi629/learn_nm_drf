
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.testcases.models import Testcases
from apps.interfaces.models import Interfaces


from utils import validates
from utils.validates import whether_existed_interface_id,whether_existed_project_id


class InterfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')
    # 项目id
    project_id = serializers.IntegerField(write_only=True,validators=[whether_existed_project_id],help_text='项目ID')
    # 接口id
    interface_id = serializers.IntegerField(write_only=True,validators=[whether_existed_interface_id],help_text='接口ID')

    class Meta:
        model = Interfaces
        fields = ('interface_id','name','project','project_id')

        extra_kwargs = {
            'name':{
                'read_only':True
            }
        }

    def validate(self, attrs):
        """
        校验项目id是否与接口id一致
        :param attrs:
        :return:
        """
        if not Interfaces.objects.filter(id=attrs['interface_id'],project_id=attrs['project_id'],is_delete=False).exists():
            raise serializers.ValidationError("项目和接口信息不对应")
        return attrs





class TestcasesSerializer(serializers.ModelSerializer):
    """
    测试用例序列化器
    """

    interface = InterfacesAnotherSerializer(help_text="所属接口和项目信息")

    class Meta:
        model = Testcases
        fields = ('id','name','interface','include','author','request')
        extra_kwargs = {
            'include':{
                'write_only':True
            },
            'request':{
                'write_only': True
            }
        }


    def create(self, validated_data):
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['interface_id']

        return Testcases.objects.create(**validated_data)

    def update(self,instance,validated_date):
        if 'interface' in validated_date:
            interface_dict = validated_date.pop('interface')
            validated_date['interface_id'] = interface_dict['interface_id']
        return super().update(instance,validated_date)

class TestcasesRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id','env_id')

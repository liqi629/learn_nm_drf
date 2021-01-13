

from rest_framework import serializers


from apps.interfaces.models import Interfaces
from utils.validates import whether_existed_project_id, whether_existed_interface_id
from apps.configures.models import Configures



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
            'interface_id':{
                'write_only':True
            },
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



class ConfiguresSerializer(serializers.ModelSerializer):
    """
    配置序列化器
    """
    interface = InterfacesAnotherSerializer(help_text='项目id和接口id')

    class Meta:
        model = Configures
        fields = ('id', 'name','interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }



    def create(self, validated_data):
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['interface_id']
        return Configures.objects.create(**validated_data)

    def update(self,instance,validated_date):
        if 'interface' in validated_date:
            interface_dict = validated_date.pop('interface')
            validated_date['interface_id'] = interface_dict['interface_id']
        return super().update(instance,validated_date)


